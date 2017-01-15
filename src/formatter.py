from .command import Command
from .settings import Settings


class Formatter(object):
    def __init__(self, name=None, source=None, binary=None):
        self.__name = name
        self.__source = 'source.' + (source if source else name.lower())
        self.__binary = binary
        self.__settings = Settings(name.lower())

    @property
    def settings(self):
        return self.__settings

    @property
    def name(self):
        return self.__name

    @property
    def source(self):
        return self.__source

    @property
    def binary(self):
        return self.settings.get('binary', self.__binary)

    @property
    def options(self):
        return self.settings.get('options', {})

    @property
    def format_on_save(self):
        return self.settings.get('format_on_save', False)

    @format_on_save.setter
    def format_on_save(self, value):
        self.settings.set('format_on_save', value)

    def command(self):
        return [self.binary]

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return [file_name]

    def parsed_options(self):
        options = []
        for key, value in self.options.items():
            options.extend(['--' + key, value])
        return options

    def format(self, file=None, input=None):
        command = self.command()
        options = self.parsed_options()
        args = self.file_args(file) if file else self.selection_args()
        return Command(command + options + args).run(input)
