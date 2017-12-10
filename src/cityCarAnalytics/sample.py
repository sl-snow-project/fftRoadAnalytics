import numpy as np
import pandas as pd
import sys
import os

TH = 10000

class Sample:
    def __init__(self,x1,y1,x2,y2):

        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.path_cou = 0
        self.noise_cou = 0
        self.id = []
        self.x1 = []
        self.x2 = []
        self.y1 = []
        self.y2 = []
        self.noise = []
        self.prev = ""

    def search(self,longitude,latitude,noise,id):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        for i in range(len(longitude)):
            if (longitude[i] <= x2) & (longitude[i] >= x1) & (latitude[i] >= y2) & (latitude[i] <= y1):
                if self.prev != id[i]:
                    self.prev = id[i]
                    self.id.append(id[i])
                self.path_cou += 1
                if noise[i] > TH:
                    self.noise_cou += 1


if __name__ == "__main__":
    #sys.argv[1]は、入力するcsvデータ
    df = pd.read_csv(sys.argv[1], sep = ',', dtype = 'object')
    #sys.argv[2]はx1,sys.argv[3]はx2,sys.argv[4]はy1,sys.argv[5]はy2
    tmp = Sample(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

    for carname in df.car_name.unique():
        uniqcar_df = df.query('car_name=="'+carname+'"')
        latitude = uniqcar_df.latitude
        longitude = uniqcar_df.longitude
        id = uniqcar_df.car_name
        noise = uniqcar_df.accel_z_vertical
        tmp.search(longitude = list(map(float,longitude)),latitude = list(map(float,latitude)),noise = list(map(float,noise)),id = list(id))


    tmp_df = pd.DataFrame({"ID" : tmp.id, "path_count" : tmp.path_cou,"noise_count" : tmp.noise_cou})
    tmp_df.to_csv("sample.csv")
