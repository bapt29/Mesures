import threading
import socketserver
import os
import sys
from daemon import Daemon
from configuration import Configuration
from afficheur import Afficheur


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
        while True:
            data = self.request.recv(1024)

            if not data:
                return

            if data[0] == 0x01:  # Reboot
                os.popen('reboot -f')
                print("Reboot")

            elif data[0] == 0x02:  # Reset
                os.popen('/opt/switch_part.sh')
                print("Reset")

            elif data[0] == 0x03:  # Display message
                print("Message")
                config = Configuration('config.ini', '/var')
                aff = Afficheur(config.read_config('Afficheur', 'ip_address'), int(config.read_config('Afficheur', 'port')))
                aff.msg(data[1:].decode())

            elif data[0] == 0x04:
                print("List file")
                os.popen('python3.4 /opt/ListFile.py')

            else:
                print("Unknown function code")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def serv():
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

class MyDaemon(Daemon):
    def run(self):
        serv()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/server-dialogue.pid')
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon.start()
        elif sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
