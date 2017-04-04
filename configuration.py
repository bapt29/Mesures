import os
import configparser


class Configuration:

    def __init__(self, configuration_path, configuration_name):
        self._config = configparser.ConfigParser()
        self._configuration_name = configuration_name

        if os.path.exists(configuration_path):
            os.chdir(configuration_path)

    def read_config(self, section, option):
        try:
            self._config.read(self._configuration_name)

            if self._config.has_section(section) and self._config.has_option(section, option):
                return self._config[section][option]

            elif self._config.has_option('DEFAULT', option):
                return self._config['DEFAULT'][option]
        except IOError:
            self.init_config()

    def write_config(self, section, option, value):
        self._config[section][option] = value

        with open('config.ini', 'w') as config_file:
            self._config.write(config_file)

    def init_config(self):
        self._config['DEFAULT'] = {}
        self._config['DEFAULT']['MeasureInterval'] = '1'

        self._config['SERVER'] = {'IpAddress': '172.20.50.19',
                                  'Port': '1234'
                                  }

        self._config['SENSORS'] = {'hih6130_address': '0x27',
                                   'tmp102_address': '0x48',
                                   'raindrop_input': '2',
                                   'soil_moisture_input': '1',
                                   'boucle_pin': '18'
                                   }

        self._config['DATABASE'] = {'file_name': 'database.db',
                                    'file_path': ''
                                    }

        with open('config.ini', 'w+') as config_file:
            self._config.write(config_file)
