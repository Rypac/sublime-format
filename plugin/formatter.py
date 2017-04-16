from .base import Formatter as BaseFormatter
from .command import ShellCommand
from .settings import FormatterSettings


class Formatter(BaseFormatter):
    def __init__(self, name, formatter, settings=None):
        super().__init__(name, formatter=formatter)
        self.__settings = settings or FormatterSettings(name.lower())

    @property
    def sources(self):
        return self.__settings.sources

    @property
    def format_on_save(self):
        return self.__settings.format_on_save

    @format_on_save.setter
    def format_on_save(self, value):
        self.__settings.format_on_save = value


class ExternalFormatter(Formatter):
    def __init__(self, name, command='', args='', settings=None):
        settings = settings or FormatterSettings(name.lower())
        command = command.split(' ') if command else []
        options = settings.options
        args = args.split(' ') if args else []
        shell_command = ShellCommand(command + options + args).run
        super().__init__(name, formatter=shell_command, settings=settings)
