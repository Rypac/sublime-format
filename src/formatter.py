import json
from collections import OrderedDict
from .command import Command
from .settings import FormatterSettings


class Formatter():
    def __init__(self, name, command='', args=''):
        self.__name = name
        self.__command = command.split(' ') if command else []
        self.__args = args.split(' ') if args else []
        self.__settings = FormatterSettings(name.lower())

    @property
    def name(self):
        return self.__name

    @property
    def sources(self):
        return self.__settings.sources

    @property
    def options(self):
        return self.__settings.options

    @property
    def format_on_save(self):
        return self.__settings.format_on_save

    @format_on_save.setter
    def format_on_save(self, value):
        self.__settings.format_on_save = value

    def format(self, input):
        command = self.__command
        options = self.options
        args = self.__args
        return Command(command + options + args).run(input)


class JsonFormatter(Formatter):
    def __init__(self):
        super().__init__(name='JSON')

    def format(self, input):
        try:
            data = json.loads(input, object_pairs_hook=OrderedDict)
            return json.dumps(data, indent=4), None
        except ValueError:
            return None, 'Invalid JSON'
