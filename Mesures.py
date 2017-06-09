import smbus
import RPi.GPIO as GPIO

from ABE_ADCDACPi import ADCDACPi

class Mesures:
    __count_raindrop = 0
    __count_soil_moisture = 0

    def __init__(self, sensors, configuration):

        for sensor in sensors:
            setattr(self, sensor, None)

        for name, value in configuration.items():
            setattr(self, name, int(value))

        self.__bus = smbus.SMBus(1)
        self.__adcdac = ADCDACPi()
        self.__adcdac.set_adc_refvoltage(3.3)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.boucle_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def __del__(self):
        GPIO.cleanup(self.boucle_pin)

    def __getattribute__(self, item):
        method_name = 'get_{}'.format(item)

        if method_name in dir(Mesures):
            setattr(self, item, object.__getattribute__(self, method_name)())

        return object.__getattribute__(self, item)

    def get_air_humidity(self):
        try:
            data = self.__bus.read_i2c_block_data(self.hih6130_address, 0x00, 4)
        except IOError:
            return -250.0

        msb_humidity = data[0] & 0x3F
        lsb_humidity = data[1]
        air_humidity = msb_humidity << 8 | lsb_humidity
        air_humidity = air_humidity / 16385 * 100

        return air_humidity

    def get_air_temperature(self):
        try:
            data = self.__bus.read_i2c_block_data(self.hih6130_address, 0x00, 4)
        except IOError:
            return -250.0

        msb_temperature = data[2]
        lsb_temperature = data[3]
        air_temperature = (msb_temperature << 8 | lsb_temperature) >> 2
        air_temperature = (air_temperature / 16385) * 165 - 40

        return air_temperature

    def get_soil_temperature(self):
        try:
            data = self.__bus.read_i2c_block_data(self.tmp102_address, 0x00, 2)
        except IOError:
            return -250.0

        soil_temperature = (data[0] << 8 | data[1]) >> 4
        soil_temperature *= 0.0625

        return soil_temperature

    def get_soil_moisture(self):
        try:
            soil_moisture = self.__adcdac.read_adc_voltage(self.soil_moisture_input, 0)
        except IOError:
            return -250.0

        if soil_moisture < 0.5 and Mesures.__count_soil_moisture <= 10:
            Mesures.__count_soil_moisture += 1

            return (3.3 - soil_moisture) / 3.3 * 100
        elif Mesures.__count_soil_moisture > 10 and soil_moisture < 0.7:
            return -250.0
        else:
            Mesures.__count_soil_moisture = 0
            return (3.3 - soil_moisture) / 3.3 * 100

    def get_raindrop(self):
        try:
            raindrop = self.__adcdac.read_adc_voltage(self.raindrop_input, 0)
        except IOError:
            Mesures.__count_raindrop += 1
            return -250.0

        if raindrop < 0.5 and Mesures.__count_raindrop <= 10:
            Mesures.__count_raindrop += 1

            return (3.3 - raindrop) / 3.3 * 100
        elif Mesures.__count_raindrop > 10 and raindrop < 0.7:
            return -250.0
        else:
            Mesures.__count_raindrop = 0
            return (3.3 - raindrop) / 3.3 * 100

    def get_boucle(self):
        return GPIO.input(self.boucle_pin)

    def event_boucle(self):
        GPIO.wait_for_edge(18, GPIO.RISING, bouncetime=300)

        return True
