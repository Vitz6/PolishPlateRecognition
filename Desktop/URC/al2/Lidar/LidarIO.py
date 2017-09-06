import serial
import ast

from Lidar.hokuyo.driver import hokuyo
from Lidar.hokuyo.tools import serial_port

#TODO  fix some security issus, try - except ->result is NULL
class LidarIO:
    laser_serial = None
    port = None
    laser = None
    result_data = {}
    data = {}
    debug = 0

    def __init__(self, port, speed, max_distance=1500):
        self.uart_port = port
        self.uart_speed = speed
        self.max_distance = max_distance

        try:
            self.laser_serial = serial.Serial(port=self.uart_port, baudrate=self.uart_speed, timeout=0.5)
            self.port = serial_port.SerialPort(self.laser_serial)
            self.laser = hokuyo.Hokuyo(self.port)

        except:
            print("Lidar: connecting with lider failed")

    def test_lidar(self):
        if (self.laser != None):
            print(self.laser.laser_on())
            print('---')
            print(self.laser.get_single_scan())
            print('---')
            print(self.laser.get_version_info())
            print('---')
            print(self.laser.get_sensor_specs())
            print('---')
            print(self.laser.get_sensor_state())
            print('---')
            print(self.laser.set_high_sensitive())
            print('---')
            print(self.laser.set_high_sensitive(False))
            print('---')
            print(self.laser.set_motor_speed(10))
            print('---')
            print(self.laser.set_motor_speed())
            print('---')
            print(self.laser.reset())
            print('---')
            print(self.laser.laser_off())
        else:
            print("Laser not set")

    def process_normalization(self, data):
        result_data = {}
        for k, v in data.items():
            k_tmp = int(round(k))
            if v <= self.max_distance:
                result_data[k_tmp] = int(v)
            else:
                result_data[k_tmp] = -1
        return result_data

    def process_fill_the_gap(self, data):
        min_key = min(data.keys())
        max_key = max(data.keys())
        print((min_key))
        print((max_key))

        for i in range(min_key, max_key):
           # print(i)
            j = i
            while i not in data:
                try:
                    data[i] = data[j + 1]
                except:
                    pass
                j += 1
        return data

    def process(self, debug_data=None):
        if not self.debug:
            print(self.laser.laser_on())
            data = self.laser.get_single_scan()
        else:
            data = debug_data

        data = self.process_normalization(data)
        data = self.process_fill_the_gap(data)

        if not self.debug:
            print(self.laser.laser_off())
        return data

    def get_processed_data(self):
        processed_data = self.process()
        return processed_data


### Example
def lidar_main():
    lidar_tmp = LidarIO("COM5", 19200)
    # lidar_tmp.test_lidar()
    strr = str("single_log_lidar")
    file_object = open(strr, "a")
    file_object.write(str(lidar_tmp.get_processed_data()))
    file_object.write("\r\n")


### Test data processing
def test_process():
    lidar_tmp = LidarIO("COM5", 19200)
    lidar_tmp.debug = 1  # debug
    strr = str("single_log_lidar")
    file_object = open(strr, "r")
    data = file_object.read()
    data = ast.literal_eval(data)
    print(type(data))
    result = lidar_tmp.process(data)
    print(result)
    print((len(result)))


#test_process()
