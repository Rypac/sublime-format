import json
from collections import OrderedDict
from .command import ShellCommand
from .settings import FormatterSettings


class Formatter:
    def __init__(self, name, command='', args='', formatter=None):
        self.__name = name
        self.__settings = FormatterSettings(name.lower())
        if formatter:
            self.__format = formatter
        else:
            command = command.split(' ')
            options = self.__settings.options
            args = args.split(' ')
            self.__format = ShellCommand(command + options + args).run

    @property
    def name(self):
        return self.__name

    @property
    def sources(self):
        return self.__settings.sources

    @property
    def format_on_save(self):
        return self.__settings.format_on_save

    @format_on_save.setter
    def format_on_save(self, value):
        self.__settings.format_on_save = value

    def format(self, input):
        return self.__format(input)


class JsonFormatter(Formatter):
    def __init__(self):
        def format_json(input):
            try:
                data = json.loads(input, object_pairs_hook=OrderedDict)
                return json.dumps(data, indent=4), None
            except ValueError:
                return None, 'Invalid JSON'

        super().__init__(name='JSON', formatter=format_json)
