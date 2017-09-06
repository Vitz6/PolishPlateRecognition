
import math
import csv
import ast

from threading import Thread

from IMUd import Visualization


#for testing
import re

#import Kalman
#from pykalman import KalmanFilter
#import numpy as np

#kalmanX = Kalman(0.001, 0.003, 0.03)
#kalmanY = Kalman(0.001, 0.003, 0.03)


acc_x_calibration = 0
acc_y_calibration = 0
acc_z_calibration= 0

class IMU:

    #debug = False

    class Acc: #m/s
        acc_x = None
        acc_y = None
        acc_z = None
        acc_x_calibration = 0
        acc_y_calibration = 0
        acc_z_calibration= 0

        def __init__(self, acc_data):
            self.acc_x = float(acc_data[0]) - self.acc_x_calibration
            self.acc_y = acc_data[1] - self.acc_y_calibration
            self.acc_z = acc_data[2] - self.acc_z_calibration
            #TODO normalization
            pass

        def calibration(self):
            [self.acc_x_calibration, self.acc_y_calibration, self.acc_z_calibration] = [self.acc_x, self.acc_y, self.acc_z]

        def get_values_list(self):
            return self.acc_x, self.acc_y, self.acc_z

    class Gyr: #RPM
        gyr_x = None
        gyr_y = None
        gyr_z = None

        def __init__(self, gyr_data):
            self.gyr_x,   self.gyr_y,   self.gyr_z = gyr_data
            #TODO normalization


    class Mag: #Gauss
        mag_x = None
        mag_y = None
        mag_z = None
        alpha_direction = None #TODO change name

        def __init__(self, mag_data):
            self.mag_x ,  self.mag_y,  self.mag_z = mag_data
            self.alpha_direction= math.atan(self.mag_y,  self.mag_x)

            #TODO TO DEGRESS


            while self.alpha_direction > 2 * math.pi:
                self.alpha_direction -= 2 * math.pi

            while self.alpha_direction < 0:
                self.alpha_direction += 2 * math.pi



    class RPY:
        roll = None # x
        pitch = None # y
        yaw = None # z

        def __init__(self, acc):
            # TODO check mathematical model
            self.pitch = -(math.atan2(acc.acc_x, math.sqrt(acc.acc_y * acc.acc_y + acc.acc_z * acc.acc_z)) * 180.0) / math.pi
            self.roll = (math.atan2(acc.acc_y, acc.acc_z) * 180.0) / math.pi
            self.yaw = 180 * math.atan(acc.acc_z / math.sqrt(acc.acc_x * acc.acc_x + acc.acc_z * acc.acc_z)) / math.pi
            pass

        def __print(self):
            result = "no data"
            try:
                x_str = str(self.roll)
                y_str = str(self.pitch)
                z_str = str(self.yaw)
                result = "x: " + x_str + " y: " + y_str + " z: " + z_str
            except:
                pass
            return result

        def get_values_list(self):
            return [self.roll, self.pitch, self.yaw]


    def __init__(self, raw_data):
        self.rpy = None
        self.raw_data = raw_data
        print((len(self.raw_data)))
        if (len(self.raw_data) == 9):
            self.acc = self.Acc(raw_data[0:3])
            self.gyr = self.Gyr(raw_data[4:7])
            self.mag = self.Gyr(raw_data[6:9])

            self.rpy = self.RPY(self.acc)
            #rpy_kalman = self.kalman(rpy, gyr)


    def kalman(self, rpy, gyr):
        # kal_pitch = kalmanY.update(rpy.pitch, gyr.gyr_y);
        # kal_roll = kalmanX.update(rpy.roll, gyr.gyr_x);
        # kal_yaw = kalmanZ.update(rpy.yaw, gyr.gyr_z);

        #TODO kalaman funtion

        pass

    def get_rpy(self):
        return self.rpy

    def get_acc(self):
            return self.acc

#Test from log
data = []
with open('StorageService_2017-08-16-1.csv', 'r+') as csvfile:
    raw_data = csv.reader(csvfile, delimiter=',' , dialect='excel')
    for row in raw_data:
        if row and row[2] == "IMU":
            a = ((ast.literal_eval(row[3:12][0])))
            data.append(a)

print(data)
#Usage

imu = IMU(data[1])
imu.get_acc().calibration() #TODO zmienic pdoejscie do kalibracji, bo teraz nie jest uwzględnia poniewaz zawsze tworzy sie mowa intancja
# np zrobiec dane kalibracji jako statyczne lub zrobic IMU.update()
rpy = imu.get_rpy().get_values_list()
print((rpy))


#Visualization
vis = Visualization.Visualization()
vis.rotate_rpy(rpy)



