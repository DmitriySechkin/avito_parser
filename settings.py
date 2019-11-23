from configobj import ConfigObj
import os


class ConfigHandler:

    def __init__(self, path="Settings.ini", create_file=False):
        self.path = path
        self.config = ConfigObj()

        if self.__is_file_config():
            self.config = ConfigObj(self.path)

        elif not self.__is_file_config() and create_file:
            self.__create_new_file()

        else:
            raise Exception("No file {} found in work directory!".format(path))

    def get_setting_param(self, sections_names, name_param):
        """
        getting settings value
        :param sections_names: name of section
        :param name_param: name of settings
        :return: settings value
        """
        section = self.config

        for section_name in sections_names:
            section = self.__get_section(section, section_name, create_new_section=False)

        return section[name_param]

    def set_setting_param(self, sections_names, name_param, value):
        """
        writes setting_param in config file
        :param sections_names: name of section
        :param name_param: name of setting
        :param value: value of setting
        """

        section = self.config

        for section_name in sections_names:
            section = self.__get_section(section, section_name)

        section[name_param] = value

        self.config.write()

    def __is_file_config(self):
        """
        checks for the existence of the file
        :return: Bool
        """
        return os.path.exists(self.path)

    @staticmethod
    def __get_section(cls, section, section_name, create_new_section=True):
        """
        getting a section by section's name
        :param section: object of config section
        :param section_name: name of section
        :return: the required section
        """

        if section_name in section.sections:
            return section[section_name]

        elif not section_name in section.sections and create_new_section:
            section[section_name] = {}
            return section[section_name]

        else:
            raise

    def __create_new_file(self):
        """
        creating empty config file
        """
        print('Creating of file {0}'.format(self.path))

        self.config.filename = self.path
        self.config.write()


class ConfigSettings:

    def __init__(self):
        self._reader = ConfigHandler()
        self.login = self._reader.get_setting_param('CredentialsSudir', 'login')
        self.psw = self._reader.get_setting_param('CredentialsSudir', 'psw')
        self.domain = self._reader.get_setting_param('CredentialsSudir', 'domain')
        self.url = self._reader.get_setting_param('BaseUrl', 'url')
