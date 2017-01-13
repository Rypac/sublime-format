from ..settings import settings


class Formatter(object):
    def __init__(self, name=None, binary=None):
        self.__name = name
        self.__binary = binary

    def settings(self):
        return settings().get(self.__name, {})

    @property
    def format_on_save(self):
        return self.settings().get('format_on_save', False)

    @format_on_save.setter
    def format_on_save(self, value):
        return self.settings().set('format_on_save', value)

    def binary(self):
        return self.settings().get('binary', self.__binary)

    def command(self):
        return [self.binary()]

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return [file_name]
