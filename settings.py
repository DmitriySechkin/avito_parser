import configparser
import os


class ConfigReader:
    config = configparser.ConfigParser()

    def __init__(self, path="Settings.ini"):
        self.path = path

        if self.__is_file_config():
            self.reader = self.__get_config_from_file()
        else:
            raise Exception("No file <Settings.ini> found in work directory!")

    def get_setting_param(self, section, name_param):
        """
        getting settings value
        :param section: name of section
        :param name_parametr: name of settings
        :return: settings value
        """
        param_value = self.reader.get(section, name_param)

        if param_value != '':
            return param_value
        else:
            raise Exception("Settings value {} is empty!".format(name_param))

    def __get_config_from_file(self):
        """
        getting settings from file
        :return: объект с настройками
        """

        self.config.read(self.path)

        return self.config

    def __is_file_config(self):
        """
        проверяет существует ли файл в рабочем каталоге
        :return: boolean значение
        """
        return os.path.exists(self.path)


class ConfigSettings:

    def __init__(self):
        self._reader = ConfigReader()
        self.login = self._reader.get_setting_param('CredentialsSudir', 'login')
        self.psw = self._reader.get_setting_param('CredentialsSudir', 'psw')
        self.domain = self._reader.get_setting_param('CredentialsSudir', 'domain')
        self.url = self._reader.get_setting_param('BaseUrl', 'url')
