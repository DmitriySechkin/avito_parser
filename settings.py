from configobj import ConfigObj
import os


class ConfigReader:

    def __init__(self, path="Settings.ini", create_file=False):
        self.path = path
        self.config = ConfigObj()

        if self.__is_file_config():
            self.config = ConfigObj(self.path)

        elif not self.__is_file_config() and create_file:
            self.__create_new_file()

        else:
            raise Exception("No file {} found in work directory!".format(path))

    def get_setting_param(self, section, name_param):
        """
        getting settings value
        :param section: name of section
        :param name_parametr: name of settings
        :return: settings value
        """
        if section in self.config.keys():
            param_value = self.config[section][name_param]

            if param_value != '':
                return param_value
            else:
                raise Exception("Settings value {0} is empty!".format(name_param))

        else:
            raise Exception("Section {0} is not in file {1}!".format(section, self.path))


    def set_setting_param(self, section, name_param, value):
        """
        writes setting_param in config file
        :param section: name of section
        :param name_param: name of setting
        :param value: value of setting
        """

        if self.config[section]:
            self.config[section] = value

    def __is_file_config(self):
        """
        checks for the existence of the file
        :return: boolean value
        """
        return os.path.exists(self.path)

    def __create_new_file(self):

        # create empty config file

        print('Creating of file {0}'.format(self.path))

        self.config.filename = self.path
        self.config.write()


class ConfigSettings:

    def __init__(self):
        self._reader = ConfigReader()
        self.login = self._reader.get_setting_param('CredentialsSudir', 'login')
        self.psw = self._reader.get_setting_param('CredentialsSudir', 'psw')
        self.domain = self._reader.get_setting_param('CredentialsSudir', 'domain')
        self.url = self._reader.get_setting_param('BaseUrl', 'url')

def test():
    s = ConfigReader(create_file=True)
    v = s.get_setting_param('1','1')
    print(s)

test()