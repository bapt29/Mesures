import threading
import socketserver
import os
from configuration import Configuration
from afficheur import Afficheur
from time import sleep

def getMacAddress(interface='eth0'):
    adressemac = str(os.popen('ifconfig ' + interface + ' | grep -o -E \'([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}\'').readline())

    if len(adressemac) == 17:
        return adressemac
    else:
        if len(adressemac) > 17:
            return adressemac[:-(len(adressemac) - 17)]
        if len(adressemac) < 17:
            raise ValueError('MacAddress trop petite')


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)

        mac_address = str()

        try:
            mac_address = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(data[0], data[1], data[2], data[3], data[4], data[5])
            mac_address = mac_address.upper()
        except IndexError:
            print("no mac address")

        if mac_address == getMacAddress() or mac_address == getMacAddress('wlan0'):
            if data[6] == 0x00:  # Reboot
                #os.popen('reboot')
                print("Reboot")

            elif data[6] == 0x01:  # Reset
                #os.popen('/opt/switch_part.sh')
                print("Reset")

            elif data[6] == 0x02:  # Display message
                print("Message")
                config = Configuration('config.ini', '/var')
                aff = Afficheur(config.read_config('Afficheur', 'ip_address'), int(config.read_config('Afficheur', 'port')))
                aff.msg(data[7:30].decode())

            elif data[6] == 0x06:
                print("List file")
                os.popen('python3.4 ListFile.py')

            else:
                print("Unknown function code")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '', 1995
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    print("with ip :", ip)
    print("with port :", port)
    server.serve_forever()
