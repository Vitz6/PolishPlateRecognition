from Common.SensorResultModel import *
from GPS.pyroute.pyroutelib2.loadOsm import LoadOsm
from GPS.pyroute.pyroutelib2.route import Router
import math


class GpsPathFinder(object):
    def __init__(self, fileName, highWayType):
        self.openStreetMapData = LoadOsm(highWayType)
        self.openStreetMapData.loadOsm(fileName)

    def definePath(self, startPoint, stopPoint):
        self.startPointLat = startPoint[0]
        self.startPointLon = startPoint[1]
        self.stopPointLat = stopPoint[0]
        self.stopPointLon = stopPoint[1]

    def findNearestNodeToGpsValue(self, current_gps_value):
        nearest_node = self.openStreetMapData.findNode(current_gps_value[0], current_gps_value[1])
        return (nearest_node)

    def GetRouteToTravel(self):
        self.currentNodeIndex = 0
        self.router = Router(self.openStreetMapData)
        self.start_node = self.openStreetMapData.findNode(self.startPointLat, self.startPointLon)
        self.stop_node = self.openStreetMapData.findNode(self.stopPointLat, self.stopPointLon)

        self.currentNode = self.start_node

        self.router.InitializeStartGoalPoint(self.start_node, self.stop_node)

        distance = self.router.distance(self.start_node, self.stop_node)

        print("Distance")
        print(str(distance))
        result, self.routeOsm = self.router.doRoute(self.start_node, self.stop_node)
        self.locationRoute = [[self.startPointLat, self.startPointLon]]
        if result == 'success':
            # list the nodes
            # print(self.routeOsm)

            # list the lat/long
            for i in self.routeOsm:
                node = self.openStreetMapData.rnodes[i]
                self.locationRoute.append([node[0], node[1]])

            self.locationRoute.append([self.stopPointLat, self.stopPointLon])

            # for i in self.locationRoute:
               #print("%f,%f" % (i[0], i[1]))
        else:
            print("Failed (%s)" % result)
        return self.routeOsm, self.locationRoute

    def GetNearestNodeToCurrentLocation(self, currentPosition):

        min_distance = self.router.distance(self.start_node, self.stop_node)

        nearestIndex = 0
        for i in range(0, len(self.locationRoute)):
            temp_distance = self.router.distanceBetweenTwoPoints([self.locationRoute[i][0], self.locationRoute[i][1]],
                                                                 currentPosition)

            if temp_distance <= min_distance:
                min_distance = temp_distance
                nearestIndex = i

        return self.locationRoute[nearestIndex]

    # https://www.youtube.com/watch?v=ak5c3iGzWPc
    def GetBearingFromTwoCoordinate(self, lat1, lon1, lat2, lon2):
        # Convertion to radians representation
        lat1 = lat1 * math.pi / 180
        lat2 = lat2 * math.pi / 180
        lon1 = lon1 * math.pi / 180
        lon2 = lon2 * math.pi / 180

        dLon = (lon2 - lon1)
        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

        brng = math.atan2(y, x)

        brng = brng * 180 / math.pi
        brng = (brng + 360) % 360
        brng = 360 - brng

        return brng

    def CheckCurrentPositionAtRoute(self, currentPosition, nearestNode):
        def length(v):
            return math.sqrt(v[0] ** 2 + v[1] ** 2)

        def dot_product(v, w):
            return v[0] * w[0] + v[1] * w[1]

        def determinant(v, w):
            return v[0] * w[1] - v[1] * w[0]

        def inner_angle(v, w):
            cosx = dot_product(v, w) / (length(v) * length(w))
            rad = math.acos(cosx)  # in radians
            return rad * 180 / math.pi  # returns degrees

        def angle_clockwise(A, B):
            inner = inner_angle(A, B)
            det = determinant(A, B)
            if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
                return inner
            else:  # if the det > 0 then A is immediately clockwise of B
                return 360 - inner

        try:
            stop_lat = self.openStreetMapData.rnodes[self.stop_node][0]
            stop_lon = self.openStreetMapData.rnodes[self.stop_node][1]

            distanceToGoalPoint = self.router.distanceBetweenTwoPoints(currentPosition, [stop_lat, stop_lon])
            distanceToNearestNode = self.router.distanceBetweenTwoPoints(currentPosition, nearestNode)

            bearing = self.GetBearingFromTwoCoordinate(currentPosition[0], currentPosition[1], nearestNode[0],
                                                   nearestNode[1])
            return SensorResultModel(status=ResultStatus.Success, errors=None,
                                     data=[distanceToGoalPoint, distanceToNearestNode, bearing])
        except:
            return SensorResultModel(status=ResultStatus.Failure, errors=ErrorCodes.Unexpected,
                                     data=None)

# gpsPathFinder = GpsPathFinder("map.osm", "foot")
# gpsPathFinder.definePath([49.21158, 18.74426], [49.21187, 18.74424])
# routeOSM, routeLocation = gpsPathFinder.GetRouteToTravel()
#
#
# znak = 1
# while (1):
#     # Here is place to get current location from gps
#     lat = input("Type lat")
#     lon = input("Type lon")
#
#     nearestNode = gpsPathFinder.GetNearestNodeToCurrentLocation([float(lat), float(lon)])
#
#     gpsSensorResult = gpsPathFinder.CheckCurrentPositionAtRoute([float(lat), float(lon)], nearestNode)
#     if gpsSensorResult.status == ResultStatus.Success:
#         distanceToGoalPoint = gpsSensorResult.data[0]
#         distanceToNearestNode = gpsSensorResult.data[1]
#         angle = gpsSensorResult.data[2]
#
#         print("Arithmetic Distance to goal is" + str(distanceToGoalPoint))
#         print("Distance to current nearest node in road is ", distanceToNearestNode)
#         print("angle: " + str(angle))
#
#
#
#     if distanceToGoalPoint < 0.0004:
#         break
# print("Koniec petli")


# TEST FOR BEARING ANGLE
# gpsPathFinder = GpsPathFinder("map.osm", "foot")
#
# bearing = gpsPathFinder.GetBearingFromTwoCoordinate(51.509865, -0.118092, 51.375209, -0.12291)
# print("Bearing", str(bearing))
