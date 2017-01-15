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

    @property
    def enabled(self):
        return [x for x in self.all if x.format_on_save]

    def find(self, predicate, default=None):
        return next((x for x in self.all if predicate(x)), default)

    def by_view(self, view):
        scope = view.scope_name(0) or ''
        source = next(iter(scope.split(' ')))
        return self.find(lambda x: x.source == source)

    def by_name(self, name):
        return self.find(lambda x: x.name == name)
