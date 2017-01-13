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

    def for_source(self, source):
        return next((x for x in self.all if x.source == source), None)

    def for_name(self, name):
        return next((x for x in self.all if x.name == name), None)
