import struct
import socket
import os
from Mesures import Mesures
from database import Database
from configuration import Configuration

class Client:

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__HwAddr = self.getHwAddr()
        self.__config = Configuration('config.ini')

        try:
            self.__socket.connect((self.__config.read_config('Server', 'ip_address'), int(self.__config.read_config('Server', 'port'))))
        except OSError as m:
            print("Error no connection {}".format(m))

        self.__database = Database(self.__config.read_config('Database', 'db_file_name'), self.__config.read_config('Database', 'sql_file_name'), self.__config.read_config('Database', 'path'))
        self.__sensors = self.__database.read_entries('Sensors', ['id', 'name'])
        self.__mesures = Mesures(self.__database.read_entries('Sensors', ['name']), self.__config.read_config('Mesures'))

        self.__data = bytearray()

    def __del__(self):
        self.__socket.close()

    def getHwAddr(self, interface='eth0'):
        HwAddr = str(os.popen('ifconfig ' + interface + ' | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'').readline())

        if HwAddr is not None:
            if len(HwAddr) == 17:
                HwAddr = HwAddr.split(':')
            else:
                HwAddr = HwAddr[:-(len(HwAddr) - 17)].split(':')

            return bytearray(int(h, 16) for h in HwAddr)

        else:
            raise ValueError('Interface ' + interface + ' does not exist')

    def initialisation(self):
        longitude = float(48.7)
        latitude = float(-3.5)

        self.__data = bytearray(struct.pack("<6ss2f", self.__HwAddr, bytes(0x00), longitude, latitude))
        self.send_data(15)

    def datasensor(self):
        data_size = 0

        #MAC ADDR
        for element in self.__HwAddr:
            self.__data.append(element)
        data_size += 6

        #Function Code
        self.__data.append(0x01)
        data_size += 1

        #Number of sensors
        self.__data.append(len(self.__sensors))
        data_size += 1

        #SENSOR id + value
        for dictionary in self.__sensors:
            self.__data.append(dictionary['id'])
            self.__data += struct.pack("f", getattr(self.__mesures, dictionary['name']))
            data_size += 5

        self.send_data(data_size)

    def store_datasensor(self):
        entries = []

        for dictionary in self.__sensors:
            entries.append({'sensor_id': dictionary['id'], 'value': getattr(self.__mesures, dictionary['name'])})

        self.__database.write_entries('Sensors_values', entries)

    def send_data(self, size):
        totalsent = 0

        while totalsent < size:
            sent = self.__socket.send(self.__data[totalsent:])

            if sent == 0:
                try:
                    self.__socket.close()
                    self.__socket.connect((self.__config.read_config('Server', 'ip_address'), int(self.__config.read_config('Server', 'port'))))
                except OSError:
                    self.store_datasensor()
                else:
                    self.__data = bytearray()
                    self.datasensor()

            totalsent += sent

        self.__data = bytearray()

if __name__ == "__main__":
    client = Client()
    config = Configuration('config.ini')

    client.initialisation()

    while True:
        client.datasensor()

        sleep(int(config.read_config('Main', 'measurement_interval')))
