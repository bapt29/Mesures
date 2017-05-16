import smbus
import RPi.GPIO as GPIO

from ABE_ADCDACPi import ADCDACPi


class Mesures:

    def __init__(self, sensors, configuration):

        for sensor in sensors:
            setattr(self, sensor, None)

        for name, value in configuration.items():
            setattr(self, '__' + name, value)

        self.__bus = smbus.SMBus(1)
        self.__adcdac = ADCDACPi()
        self.__adcdac.set_adc_refvoltage(3.3)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__boucle_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def __del__(self):
        GPIO.cleanup()

    def __getattribute__(self, item):
        method_name = 'get_{}'.format(item)

        if method_name in Mesures.__dict__:
                setattr(self, item, object.__getattribute__(self, method_name)())

        return object.__getattribute__(self, item)

    def get_air_humidity(self):
        data = self.__bus.read_i2c_block_data(self.__hih6130_address, 0x00, 4)

        msb_humidity = data[0] & 0x3F
        lsb_humidity = data[1]
        air_humidity = msb_humidity << 8 | lsb_humidity
        air_humidity = air_humidity / 16385 * 100

        return air_humidity

    def get_air_temperature(self):
        data = self.__bus.read_i2c_block_data(self.__hih6130_address, 0x00, 4)

        msb_temperature = data[2]
        lsb_temperature = data[3]
        air_temperature = (msb_temperature << 8 | lsb_temperature) >> 2
        air_temperature = (air_temperature / 16385) * 165 - 40

        return air_temperature

    def get_soil_temperature(self):
        data = self.__bus.read_i2c_block_data(self.__tmp102_address, 0x00, 2)

        soil_temperature = (data[0] << 8 | data[1]) >> 4
        soil_temperature *= 0.0625

        return soil_temperature

    def get_soil_moisture(self):
        soil_moisture = self.__adcdac.read_adc_voltage(self.__soil_moisture_input, 0)

        soil_moisture = (3.3 - soil_moisture) / 3.3 * 100

        return soil_moisture

    def get_raindrop(self):
        raindrop = self.__adcdac.read_adc_voltage(self.__raindrop_input, 0)

        raindrop = (3.3 - raindrop) / 3.3 * 100

        return raindrop

    def get_boucle(self):
        return GPIO.input(self.__boucle_pin)
