from .formatters import *


class FormatRegistry():
    def __init__(self):
        self.__registered_formatters = [
            ElmFormat(), GoFormat(), JavaScriptFormat(), PythonFormat(),
            RustFormat(), TerraformFormat()
        ]

    @property
    def all(self):
        return self.__registered_formatters

    def find(self, predicate, default=None):
        return next((x for x in self.all if predicate(x)), default)

    def by_source(self, source):
        return self.find(lambda x: x.source == source)

    def by_name(self, name):
        return self.find(lambda x: x.name == name)
