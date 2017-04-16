from .command import ShellCommand


class Formatter:
    def __init__(self, name, sources=[], format_on_save=False, formatter=None):
        self.__name = name
        self.__sources = sources
        self.__format_on_save = format_on_save
        self.__format = formatter

    @property
    def name(self):
        return self.__name

    @property
    def sources(self):
        return self.__sources

    @property
    def format_on_save(self):
        return self.__format_on_save

    @format_on_save.setter
    def format_on_save(self, value):
        self.__format_on_save = value

    def format(self, input):
        return self.__format(input)


class ExternalFormatter(Formatter):
    def __init__(self, name, command='', *args, **kwargs):
        args = command.split(' ') if command else []
        formatter = ShellCommand(args).run
        super().__init__(name, formatter=formatter, *args, **kwargs)
