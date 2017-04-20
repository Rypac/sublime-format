from .command import ShellCommand
from .settings import FormatterSettings


class Formatter:
    def __init__(self, name, sources=None, formatter=None, settings=None):
        self.__name = name
        self.__sources = sources
        self.__settings = settings or FormatterSettings(name.lower())
        self.__format = formatter

    @property
    def name(self):
        return self.__name

    @property
    def settings(self):
        return self.__settings

    @property
    def sources(self):
        return self.__sources or self.settings.sources

    @property
    def format_on_save(self):
        return self.settings.format_on_save

    @format_on_save.setter
    def format_on_save(self, value):
        self.__settings.format_on_save = value

    def format(self, input, *args, **kwargs):
        return self.__format(input, *args, **kwargs)


class ExternalFormatter(Formatter):
    def __init__(self, name, command='', args='', *aargs, **kwargs):
        self.__command = command.split(' ') if command else []
        self.__args = args.split(' ') if args else []
        super().__init__(name, *aargs, **kwargs)

    def command(self):
        args = self.__command + self.settings.options + self.__args
        return ShellCommand(args)

    def format(self, input, *args, **kwargs):
        return self.command().run(input)
