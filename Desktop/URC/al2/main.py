import datetime
import logging
import time

from GPS.GpsPathFinder import GpsPathFinder, ResultStatus


from IO.IO import IO
from IO.CommunicationService import CommunicationService, PacketsSend, PacketsRecv
from IO.StorageService import StorageService


class MainAutoControll:
    missionCords = []

    def __init__(self, communicationMode=None, logLevel=logging.DEBUG, logFile='logs.log'):
        self.isSuccessfullyInitialized = True
        try:
            self.io = IO(*communicationMode,
                         storagePath="storage\\", storageFilename=None,
                         logFile=logFile, logLevel=logLevel)
            self.io.loggerWrapper.logInfo("MainAutoControll ctor started")

            self.initGpsPathFinder()

        except Exception as e:  # todo: error handling!
            self.isSuccessfullyInitialized = False
            self.io.loggerWrapper.logError("Unknown error during autoRover starting: " + str(e))

    def initGpsPathFinder(self):
        # gps path finder
        self.gpsPathFinder = GpsPathFinder("map.osm", "foot")

        # ustalanie trasy dla danego przejazdu
        self.gpsPathFinder.definePath([50.01824, 21.98584], [50.01837921142578, 21.986557006835984])
        self.routeOSM, self.routeLocation = self.gpsPathFinder.GetRouteToTravel()

    # todo: MOVE TO GPS SERVICE!
    def moveByGPS(self, gps):
        # Here is place to get current location from gps
        lat = gps[1][1]
        lon = gps[1][0]

        print("lat: " + str(lat) + " | lon: " + str(lon))
        nearestNode = self.gpsPathFinder.GetNearestNodeToCurrentLocation([float(lat), float(lon)])

        try:
            gpsSensorResult = self.gpsPathFinder.CheckCurrentPositionAtRoute([lat, lon], nearestNode)
            if gpsSensorResult.status == ResultStatus.Success:
                distanceToGoalPoint = gpsSensorResult.data[0]
                distanceToNearestNode = gpsSensorResult.data[1]
                angle = gpsSensorResult.data[2]
                print("Arithmetic Distance to goal is" + str(distanceToGoalPoint))
                print("Distance to current nearest node in road is ", distanceToNearestNode)
                print("angle: " + str(angle))

                angle *= 5000
                # Temp TODO MOVE DECISION OF ROVER DRIVING TO "COMMON SENSOR GUARDIAN" (Name is temp)
                isGoalReached = distanceToGoalPoint <= 0.00004
                if not isGoalReached:
                    print("Goal is not reached")
                    self.io.communicationService.sendPacket(PacketsSend.RightLeftDriving, (
                        50.0 - 50 * angle, 55.0 + 50 * angle))  # right/left levels (-100, 100)

        except Exception as e:  # todo: error handling!
            print(e)

    def mainLoop(self):
        if not self.isSuccessfullyInitialized:
            return
        while True:
            time.sleep(0.001)

            if not self.io.communicationService.isCommunicationRunning:
                if not self.io.start(communication=True, storage=not self.io.storageService.isStorageInitialized()):
                    self.io.loggerWrapper.logError("Cannot connect to rover!")
                    continue

            self.io.communicationService.sendPacket(PacketsSend.RightLeftDriving,
                                                    (50.0, 55.0))  # right/left levels (-100, 100)

            gps = self.io.readGPS()
            if gps is None:
                continue
            else:
                self.moveByGPS(gps)

                # todo: add some decision making service


# communicationSerial = ("COM10", "115200", "Serial") # real
communicationSerial = ("COM1", "115200", "Serial")  # tester
communicationUDP = ("192.168.4.1", "12852", "Udp")

try:
    MainAutoControll(communicationSerial).mainLoop()
except Exception as e:
    print(e)
