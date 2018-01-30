import numpy as np
import pandas as pd
import sys
import os

TH = 60000
L = 5
lon1 = 0.000010966382364
lat1 = 0.000008983148616
#x1y1,x2y2 全体の範囲
class Sample:
    def __init__(self,x1,y1,x2,y2):

        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        lenx = abs(self.x2 - self.x1) / (L*lon1)
        leny = abs(self.y2 - self.y1) / (L*lat1)
        lenx = int(lenx) + 100
        leny = int(leny) + 100
        #print(lenx,leny)
        self.li_noise = [[-1 for i in range(lenx)] for j in range(leny)]
        self.li_path = [[-1 for i in range(lenx)] for j in range(leny)]
        self.li_ans = [[-1 for i in range(lenx)] for j in range(leny)]




    def search(self,longitude,latitude,noise):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        # 1mあたり緯度 : 0.000008983148616
        # 1mあたり経度 : 0.000010966382364


        for i in range(len(longitude)):
            locx = ((longitude[i] / lon1) - (x1 / lon1)) / L
            locy = ((latitude[i] / lat1) - (y1 / lat1)) / L
            #print(x1,x2,y1,y2)
            if locx >= x1 and locx <= x2 and locy >= y1 and locy <= y2:
                li_path[locx][locy] += 1;

                if noise[i] > TH:
                    li_noise[locx][locy] += 1;


        #ans = noise_cou / path_cou
        #for i in range(int(x1),int(x2),L):
        #    for j in range(int(y1),int(y2),L):
        print(range(int(abs(x1-x2)/(L*lon1))))
        print(range(int(abs(y1-y2)/(L*lon1))))
        for i in range(int(abs(x1-x2)/(L*lon1))):
            for j in range(int(abs(y1-y2)/(L*lat1))):
                try:
                    if self.li_path[i][j] > 0:
                        self.li_ans[i][j] = self.li_noise[i][j] / self.li_path[i][j]
                        print("a")
                        print(self.li_ans[i][j])
                except:
                    print("out of range")

if __name__ == "__main__":
    #sys.argv[1]は、入力するcsvデータ
    df = pd.read_csv(sys.argv[1], sep = ',', dtype = 'object')
    #sys.argv[2]はx1,sys.argv[3]はx2,sys.argv[4]はy1,sys.argv[5]はy2

    #tmp = Sample(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    tmp = Sample(37.511156,139.917766,37.498440,139.928565)
    latitude = df.latitude
    longitude = df.longitude
    noise = df.accel_z_vertical
    tmp.search(longitude = list(map(float,longitude)),latitude = list(map(float,latitude)),noise = list(map(float,noise)))


    s1 = int(tmp.x1 / L)
    e1 = int(tmp.x2 / L)
    s2 = int(tmp.y1 / L)
    e2 = int(tmp.y2 / L)
    n = e1 - s1 + e2 - s2
    #li_loc = [[0 for i in range(0,n)] for j in range(0,5)]
    li_loc = []
    for i in range(s1,e1,L):
        for j in range(s2,e2,L):
            for k in range(0,n):
                array = [i,j,i+L,j+L,tmp.li_ans[i][j]]
                # li_loc.append(li_loc,array,axis=0)
                li_loc.append(array)

            #i2 = i + L
            #j2 = j + L


    li_loc2 = np.array(li_loc)
    np.savetxt("test.csv",li_loc2)
    #tmp_df = pd.DataFrame(li_loc2,column=['x1','x2','y1','y2'])
    #tmp_df = pd.DataFrame({"x1": range(s1,e1),"y1": range(s2,e2),"ans": tmp.li_ans})
    #tmp_df.to_csv("sample.csv")
