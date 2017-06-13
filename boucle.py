import RPi.GPIO as GPIO
import sys
from database import Database
from configuration import Configuration
from daemon import Daemon

def serv():
    config = Configuration('config.ini', '/var/')
    db = Database(config.read_config('Database', 'db_file_name'), config.read_config('Database', 'sql_file_name'), config.read_config('Database', 'path'))

    boucle_pin = int(config.read_config('Mesures', 'boucle_pin'))

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(boucle_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        GPIO.wait_for_edge(boucle_pin, GPIO.RISING, bouncetime=300)
        print("1")
        db.increment_entry('Traffic', 'Traffic_count')


class MyDaemon(Daemon):
    def run(self):
        serv()

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/traffic_count.pid')
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
