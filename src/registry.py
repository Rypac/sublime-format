from .formatter import *


class FormatterRegistry():
    def __init__(self):
        self.__formatters = [
            ClangFormat(), ElmFormat(), GoFormat(), JavaScriptFormat(),
            JsonFormat(), PythonFormat(), RustFormat(), TerraformFormat()
        ]

    @property
    def all(self):
        return self.__formatters

    @property
    def enabled(self):
        return [x for x in self.all if x.format_on_save]

    def find(self, predicate, default=None):
        return next((x for x in self.all if predicate(x)), default)

    def by_view(self, view):
        source = view.scope_name(0).split(' ')[0].split('.')[1]
        return self.find(lambda x: x.source == source)

    def by_name(self, name):
        return self.find(lambda x: x.name == name)
