#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

from scipy.fftpack import fft
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np

class road_aizu_fft:
    def __init__(self, blocksize=200, normalize=True):
        self.blocksize = blocksize
        self.normalize = True
    
    def parse_fft(self, pulse_data, latitude, longitude, time):
        #if isinstance(parse_data, list) != True:
        #   print("Please input list object")

        blocksize = self.blocksize
        normalize = self.normalize

        input_data = np.array(pulse_data, dtype=np.float32)
        window_pulse = [window for window in [input_data[p:][:blocksize] for p in
                                              [i for i in range(0, np.shape(input_data)[0], int(blocksize/2))]] if len(window)==blocksize]
        #position = zip(latitude, longitude, time)
        position_arr = [i for i in range(0, np.shape(latitude)[0], int(blocksize/2))]
        
        window_fft = [fft(list(i)) for i in window_pulse]
        pulse_sum = [sum(abs(pulse)).astype(np.float32) for pulse in window_fft]
        sum_sqare = [i**2 for i in pulse_sum]

        longitude_v1 = list(longitude)
        latitude_v1  = list(latitude)
        time_arr_v1  = list(time)

        longtitude_arr = [longitude_v1[i] for i in position_arr]
        latitude_arr   = [latitude_v1[i] for i in position_arr]
        time_arr       = [time_arr_v1[i] for i in position_arr]

        return [list(i) for i in zip(sum_sqare, latitude_arr, longtitude_arr, time_arr)]

tmp = road_aizu_fft(blocksize=40)
df = pd.read_csv(".//20170220.csv")

#datetime   = df.measurement_ms

#df.index = pd.DatetimeIndex(df.measurement_ms, name='on_create').tz_localize('UTC').tz_convert('Asia/Tokyo')
#print(df)

for carname in df.car_name.unique():
    print(carname)

    uniqcar_df = df[df.car_name.str.contains(str(carname))]
    datetime   = uniqcar_df.measurement_ms
    latitude   = uniqcar_df.latitude
    longitude  = uniqcar_df.longitude
    z_vertical = uniqcar_df.accel_z_vertical-9.8

    fft_response = tmp.parse_fft(z_vertical, latitude=list(latitude), longitude=list(longitude), time=datetime)
    response_uniqcar_df = pd.DataFrame(fft_response)
    response_uniqcar_df.to_csv(str(carname) + '.csv')
