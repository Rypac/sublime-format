import json
from collections import OrderedDict
from .command import Command
from .settings import FormatterSettings


class Formatter():
    def __init__(self, name, command=None, args=None, formatter=None):
        self.__name = name
        self.__format = formatter
        self.__settings = FormatterSettings(name.lower())

        if not formatter:
            command = command.split(' ') if command else []
            options = self.__settings.options
            args = args.split(' ') if args else []
            shell_command = Command(command + options + args)

            def external_format(input):
                return shell_command.run(input)

            self.__format = external_format

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
