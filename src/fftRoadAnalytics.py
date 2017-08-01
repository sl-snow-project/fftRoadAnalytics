#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

from scipy.fftpack import fft
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
import sys
import os

class road_aizu_fft:
    def __init__(self, blocksize=40, normalize=True):
        self.blocksize = blocksize
        self.normalize = True
    
    def parse_fft(self, carname, pulse_data, latitude, longitude, time):
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

        original_pulse_sumarr = [sum(abs(i)) for i in window_pulse]

        longitude_v1 = list(longitude)
        latitude_v1  = list(latitude)
        time_arr_v1  = list(time)
        carname_v1   = list(carname)

        longtitude_arr = [longitude_v1[i] for i in position_arr]
        latitude_arr   = [latitude_v1[i] for i in position_arr]
        time_arr       = [time_arr_v1[i] for i in position_arr]
        carname_arr    = [carname_v1[i] for i in position_arr]

        return [list(i) for i in zip(carname_arr, time_arr, sum_sqare, original_pulse_sumarr, latitude_arr, longtitude_arr, window_pulse)]


dirname = ""
tmp = road_aizu_fft(blocksize=40)
# df = pd.read_csv(".//sample.csv")
df = pd.read_csv(sys.argv[1])
print(sys.argv[1])
try:
   os.mkdir(sys.argv[2])
   dirname = sys.argv[2]
except:
   os.mkdir("datetime")
   dirname = "datetime"

for carname in df.car_name.unique():
    print(carname)

    #uniqcar_df = df[df.car_name.str.contains(carname) and carname.contains(df.car_name)]
    uniqcar_df = df.query('car_name=="'+carname+'"')
    unix_date  = uniqcar_df.measurement_ms
    latitude   = uniqcar_df.latitude
    longitude  = uniqcar_df.longitude
    z_vertical = uniqcar_df.accel_z_vertical-9.8
    carid      = uniqcar_df.car_name
    datetime   = pd.to_datetime(unix_date, unit="ms")

    fft_response = tmp.parse_fft(pulse_data=z_vertical, carname=list(carid), latitude=list(latitude), longitude=list(longitude), time=datetime)
    response_uniqcar_df = pd.DataFrame(fft_response)
    response_uniqcar_df.to_csv(str(dirname)+"/"+str(carname) + '.csv')
