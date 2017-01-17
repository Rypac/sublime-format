from .formatters import *


class FormatRegistry():
    def __init__(self):
        self.__registered_formatters = [
            ClangFormat(), ElmFormat(), GoFormat(), JavaScriptFormat(),
            PythonFormat(), RustFormat(), TerraformFormat()
        ]
        self.__source_formatter_lookup_table = {}
        for formatter in self.__registered_formatters:
            self.__source_formatter_lookup_table[formatter.source] = formatter

    @property
    def all(self):
        return self.__registered_formatters

    @property
    def enabled(self):
        return [x for x in self.all if x.format_on_save]

    def find(self, predicate, default=None):
        return next((x for x in self.all if predicate(x)), default)

    def by_view(self, view):
        source = view.scope_name(0).split(' ')[0]
        return self.__source_formatter_lookup_table.get(source)

    def by_name(self, name):
        return self.find(lambda x: x.name == name)
