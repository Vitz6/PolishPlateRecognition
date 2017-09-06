
from Lidar.LidarIO import LidarIO
from Lidar.Obstacle import Obstacle

import matplotlib.pyplot as plt
import ast
import math
from threading import Thread

class Lidar2D:
    debug = None
    draw = None
    max_angle = None
    min_angle = None
    lidarIO = None

    def __init__(self, debug = 0, draw = 0):
        self.debug = debug
        self.draw = draw

        #LidarIO instance
        self.lidarIO =   LidarIO("COM5", 19200)

        if self.debug:
            self.lidarIO.debug = 1  # debug
            strr = str("single_log_lidar")
            file_object = open(strr, "r")
            data = file_object.read()
            data = ast.literal_eval(data)
            self.data = self.lidarIO.process(data)

        if not self.debug:
            self.data = self.lidarIO.get_processed_data() #TODO with connection

       # print(self.data)
        self.max_angle = max(self.data.keys())
        self.min_angle = min(self.data.keys())

        if(self.draw):
            self.draw_raw_data()


    def draw_raw_data(self):
        for i in range(self.min_angle, self.max_angle):
            xr = math.sin(math.radians(i)) * 1500
            yr = math.cos(math.radians(i)) * 1500
            plt.plot(xr, yr, 'g^')

        for i in range(self.min_angle, self.max_angle):
            # print(i)
            if self.data[i] == 0 or self.data[i] == -1:
                continue
            x = math.sin(math.radians(i)) * self.data[i]
            y = math.cos(math.radians(i)) * self.data[i]
            plt.plot(x, y, 'ro')

    # def find_nearest_obstacle(self):
    #
    #     data_tmp = {}
    #     for i in range(self.min_angle,self.max_angle):
    #         if(self.data[i] != -1):
    #             if (self.data[i] != 0):
    #                 data_tmp[i] = self.data[i]
    #     print(data_tmp)
    #     print(self.data)
    #
    #     min_distance =  min(data_tmp.values())
    #     angle = list(data_tmp.keys())[list(data_tmp.values()).index(min_distance)]
    #
    #     return [angle, min_distance] # return -1


    def find_all_obstacles(self):
        data_segmented = self.segmentation()
        obstacle_points_list_tmp = []
        continuation = 0
        obstacles_list = []

        for i in range(self.min_angle,self.max_angle):
            if(data_segmented[i] != -1 and data_segmented[i] != 0):
                if continuation == 0:
                    obstacle_points_list_tmp.append([i,data_segmented[i]])
                    continuation += 1
                else:
                    last_tmp_point = obstacle_points_list_tmp[len(obstacle_points_list_tmp) - 1][1]
                    last_current_point = data_segmented[i]
                    difference = last_tmp_point - last_current_point

                    if difference < 0:
                        difference *= -1

                    if(difference <= 50 ):
                        obstacle_points_list_tmp.append([i, data_segmented[i]])
                        continuation += 1
                    else:
                        if len(obstacle_points_list_tmp) > 1:
                            print("OBJ DETECTED!!!")
                            obstacle = Obstacle(obstacle_points_list_tmp)
                            obstacles_list.append(obstacle)
                            print("All points")
                            print(obstacle_points_list_tmp)

                            if self.draw:
                                xO = []
                                yO = []
                                for i in obstacle_points_list_tmp:
                                    xO.append(math.sin(math.radians(i[0])) * i[1])
                                    yO.append(math.cos(math.radians(i[0])) * i[1])
                                plt.plot(xO, yO, '--')

                            obstacle_points_list_tmp = []
                            continuation = 0

    def show(self):
     #   t1 = Thread(target= plt.show(), args=[])
      #  t1.start()
        plt.show()

    def segmentation(self):
        data_tmp = {}
        print(self.max_angle)
        for i in range(self.min_angle, self.max_angle):
            pass
            data_tmp[i] = int(self.data[i] / 10) * 10
        return data_tmp



lidar = Lidar2D(debug = 1, draw = 1)
print(lidar.find_all_obstacles())
lidar.show()


print("yeash")


