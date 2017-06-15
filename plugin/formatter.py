from .command import shell
from .settings import FormatterSettings, Settings


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
    def __init__(self, name, command='', args='', settings=None):
        command = command.split(' ') if command else []
        args = args.split(' ') if args else []
        settings = settings or FormatterSettings(name.lower())
        opts = settings.options or []
        formatter = shell(command + opts + args, paths=Settings.paths())
        super().__init__(name, formatter=formatter, settings=settings)
