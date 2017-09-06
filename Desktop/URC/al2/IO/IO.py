from IO.CommunicationService import CommunicationService, PacketsRecv, PacketsSend
from IO.StorageService import StorageService
from IO.LoggerWrapper import LoggerWrapper
import logging


class IO:
    def __init__(self, port, baudrate, mode, storagePath, storageFilename, logLevel, logFile):
        self.communicationService = CommunicationService(port, baudrate, mode)
        self.storageService = StorageService(storagePath, storageFilename)
        self.loggerWrapper = LoggerWrapper(logFile, logLevel)

    def start(self, communication=True, storage=True):
        if communication:
            self.communicationService.start()
        if storage:
            self.storageService.start()
        return True

    def stop(self, communication=True, storage=True):
        if communication:
            self.communicationService.stop()
        if storage:
            self.storageService.stop()

    def readGPS(self):
        return self.__readAndStore(PacketsRecv.GPS)

    def readRawImu(self):
        return self.__readAndStore(PacketsRecv.IMU)

    def __readAndStore(self, packetType: PacketsRecv):
        packet = self.communicationService.getCertainPacketNonBlocking(packetType)
        if packet is not None:
            self.storageService.store(packet, packetType._name_)
            self.loggerWrapper.logDebug("Packet of type " + packetType._name_ + " received: " + str(packet))
        return packet
