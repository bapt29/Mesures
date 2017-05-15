import os
import configparser


class Configuration:

    def __init__(self, configuration_name, configuration_path=None):
        self.__config = configparser.ConfigParser()
        self.__configuration_name = configuration_name

        if configuration_path is not None and os.path.exists(configuration_path):
            os.chdir(configuration_path)

    def read_config(self, section):
        self.__config.read(self.__configuration_name)

        return dict(self.__config.items(section))

    def write_config(self, section, option, value):
        self.__config[section][option] = value

        with open(self.__configuration_name, 'w') as config_file:
            self.__config.write(config_file)



        with open(self.__configuration_name, 'w+') as config_file:
            self.__config.write(config_file)
