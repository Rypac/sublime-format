from ..settings import Settings




class Formatter(object):
    def __init__(self, name=None, source=None, binary=None):
        self.__name = name
        self.__source = 'source.' + (source if source else name.lower())
        self.__binary = binary
        self.__settings = Settings(name.lower())

    @property
    def name(self):
        return self.__name

    @property
    def source(self):
        return self.__source

    @property
    def binary(self):
        return self.__settings.get('binary', self.__binary)

    @property
    def format_on_save(self):
        return self.__settings.get('format_on_save', False)

    @format_on_save.setter
    def format_on_save(self, value):
        self.__settings.set('format_on_save', value)

    def command(self):
        return [self.binary]

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return [file_name]
