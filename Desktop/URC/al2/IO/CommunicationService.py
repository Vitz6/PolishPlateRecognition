from IO.ComPort import ComPort
from enum import Enum
from struct import *
import _thread
import time
import threading


#  todo: add syncking!@@@!!!!!

class CommunicationService:
    def __init__(self, port, baudrate, mode, customPacketsRecv=None):
        self.comPort = ComPort(
            port,
            baudrate,
            customPacketsRecv if customPacketsRecv is not None else PacketsRecv,
            mode)
        self.isCommunicationRunning = False

        self.packetsReceived = []
        self.packetsToSend = []

    def start(self):
        self.isCommunicationRunning = False
        if self.comPort.start():
            self.isCommunicationRunning = True
            try:
                threading.Thread(target=self.communicationLoop).start()
            except Exception as e:
                print(e)
        return self.isCommunicationRunning

    def stop(self):
        self.isCommunicationRunning = False
        self.comPort.stop()

    def communicationLoop(self):
        try:
            while True:
                # print("CommunicationLoop working")
                time.sleep(0.001)
                if not self.isCommunicationRunning:
                    self.stop()
                    return

                packet = self.comPort.receive()
                if packet is not None:
                    self.packetsReceived.append(packet)
                for packetToSend in self.packetsToSend:  # todo: check if it is thread safe
                    self.comPort.send(packetToSend)
                    self.packetsToSend.remove(packetToSend)
                    # todo: add properties to get/send packet! and test
        except Exception as e:
            self.stop()

    def sendPacket(self, packetSend, data: tuple):
        # if not isinstance(packetSend, PacketsSend):
        #     raise AssertionError("packPacket received wrong packetSend parameter, given:" + type(packetSend))
        if len(data) != (len(packetSend.value[1])):
            raise AssertionError("packPacket received wrong data parameter or not enough values, given:" + type(data))

        packet = pack("=BB" + packetSend.value[1], ord(':'), int(packetSend.value[0]), *data)
        self.packetsToSend.append(packet)

    def getPacketNonBlocking(self):
        if len(self.packetsReceived) > 0:
            packet = self.packetsReceived[0]
            self.packetsReceived.remove(packet)
            return packet
        return None

    def getCertainPacketNonBlocking(self, packetType):
        if len(self.packetsReceived) > 0:
            lastCertainPacket = None
            for packet in self.packetsReceived:
                if packet[0] == packetType.value[0]:
                    lastCertainPacket = packet
                    self.packetsReceived.remove(packet)
            return lastCertainPacket
        return None

    def getPacketBlocking(self, timeoutMiliseconds=100):
        start = int(round(time.time() * 1000))
        while True:
            if len(self.packetsReceived) > 0:
                packet = self.packetsReceived[0]
                self.packetsReceived.remove(packet)
                return packet
            if int(round(time.time() * 1000)) - start > timeoutMiliseconds:
                return None
            time.sleep(0.001)


class PacketsSend(Enum):
    RightLeftDriving = (30, "ff")  # (-100, 100)


class PacketsRecv(Enum):
    GPS = (0x2a, "ddf")
    IMU = (0x29, "fffffffff")
