import time
from enum import Enum

from IO.CommunicationService import CommunicationService


class PacketsSend(Enum):
    GPS = (0x2a, "ddf")
    IMU = (0x29, "fffffffff")


class PacketsRecv(Enum):
    RightLeftDriving = (30, "ff")  # (-100, 100)


communicationSerial = ("COM2", "115200", "Serial")  # tester
communication = CommunicationService(*communicationSerial, PacketsRecv)

communication.start()

while True:
    time.sleep(1)
    if not communication.isCommunicationRunning:
        if not communication.start():
            print("can't connect")
            continue
        else:
            print("connected")

    steringValues = communication.getCertainPacketNonBlocking(PacketsRecv.RightLeftDriving)
    if steringValues is not None:
        print("Right: " + str(steringValues[0]) + " Left: " + str(steringValues[1]))

    communication.sendPacket(PacketsSend.GPS, (21.98584, 50.01824, 325))
