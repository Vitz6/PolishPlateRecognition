import os
import sys
import time
from subprocess import Popen
import socket
import socketserver
import serial
from struct import *
from collections import namedtuple


class ComPort:
    serialMode = "Serial"
    udpMode = "Udp"

    def __init__(self, port, baudrateOrIp, receivePacketSource, mode):
        self.port = port
        self.baudrate = baudrateOrIp

        self.mode = mode
        self.communicationDevice = None

        def getStructSize(format):
            size = 0
            for c in format:
                cSize = 4 if c in ['i', 'f'] else 8 if c in ['d'] else 0
                if cSize == 0:
                    raise IndexError()
                size += cSize
            return size

        # dict: packet number => packet number | format | packet structure length [bytes]

        packetList = list(receivePacketSource.__members__.items())
        self.receivePacketsNumbers = {x[1].value[0]: (x[1].value[0], x[1].value[1], getStructSize(x[1].value[1])) for x
                                      in packetList}
        self.readBuffer = []
        self.readState = 1
        self.currentPacket = None  # (length, format)

    def start(self):
        try:
            if self.mode == self.serialMode:
                self.communicationDevice = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0  # makes api non blocking
                )
            elif self.mode == self.udpMode:
                self.communicationDevice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                self.communicationDevice.settimeout(0)
                self.communicationDevice.connect((self.port, int(self.baudrate)))
                return True
            else:
                raise Exception("unknown mode")

        except IOError as e:
            return False

        return self.communicationDevice.is_open if self.communicationDevice is not None else False

    def stop(self):
        if self.communicationDevice is not None: ##and self.communicationDevice.is_open:
            self.communicationDevice.close()

    def send(self, data):
        if self.mode == self.serialMode:
            try:
                self.communicationDevice.write(data)
            except:
                pass
        elif self.mode == self.udpMode:
            self.communicationDevice.sendto(data, (self.port, int(self.baudrate)))

    def receive(self):
        if self.mode == self.serialMode:
            lastChar = self.communicationDevice.read(1)
        elif self.mode == self.udpMode:
            try:
                lastChar = None
                lastChar, addr = self.communicationDevice.recvfrom(1)
            except Exception as e:  # todo: error handling!
                pass

        if lastChar is None or len(lastChar) == 0:
            return None

        if self.readState == 1:
            self.currentPacket = None
            self.readBuffer = []

            if ord(lastChar) == ord(':'):
                self.readState = 2

        elif self.readState == 2:
            self.currentPacket = None
            self.readBuffer = []
            if ord(lastChar) in self.receivePacketsNumbers.keys():
                self.currentPacket = self.receivePacketsNumbers[ord(lastChar)]
                self.readState = 3
            else:
                self.readState = 1

        elif self.readState == 3:
            self.readBuffer.append(ord(lastChar))
            if len(self.readBuffer) == self.currentPacket[2]:
                packet = unpack(self.currentPacket[1], bytes(self.readBuffer))
                self.readState = 1
                return self.currentPacket[0], packet
            return None
        else:
            raise ValueError("Unknown state detected!")
