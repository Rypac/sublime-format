from .formatter import *


class FormatterRegistry():
    def __init__(self):
        self.__formatters = []
        self.__formatter_source_map = {}

    def populate(self):
        self.__formatters = [
            ClangFormat(), ElmFormat(), GoFormat(), JavaScriptFormat(),
            JsonFormat(), PythonFormat(), RustFormat(), TerraformFormat()
        ]
        self.__formatter_source_map = dict((source, formatter)
                                           for formatter in self.__formatters
                                           for source in formatter.sources)

    @property
    def all(self):
        return self.__formatters

    @property
    def enabled(self):
        return [x for x in self.all if x.format_on_save]

    def by_view(self, view):
        source = view.scope_name(0).split(' ')[0].split('.')[1]
        return self.__formatter_source_map.get(source)

    def by_name(self, name):
        return next((x for x in self.all if x.name == name))
