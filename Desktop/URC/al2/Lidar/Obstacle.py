

class Obstacle:
    middle_point = None
    distance_to_middle_point = None
    size = 0
    variation = 0 #TODO later

    def __init__(self, points_list):

        self.size = len(points_list)
        if self.size % 2:
            middle = int(self.size/2 )
        else:
            middle = int(self.size/2) -1

        self.middle_point = points_list[middle]

        self.distance_to_middle_point = self.middle_point[1]


    def get_middle_point(self):
        return self.middle_point

    def get_distance_to_middle_point(self):
        return self.distance_to_middle_point

    def get_size(self):
        return self.size

    def __print_all(self):
        print("Size")
        print(self.size)
        print("Middle")
        print(self.middle_point)
        print("Middle [mm]")
        print(self.distance_to_middle_point)






