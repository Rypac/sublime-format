from .formatter import ExternalFormatter, Formatter
from .formatters import format_json


class FormatterRegistry:
    def __init__(self):
        self.__formatters = []

    def populate(self):
        self.__formatters = [
            ExternalFormatter('Clang', command='clang-format'),
            ExternalFormatter('Elm', command='elm-format', args='--stdin'),
            ExternalFormatter('Go', command='gofmt'),
            ExternalFormatter('Haskell', command='hindent'),
            ExternalFormatter(
                'JavaScript', command='prettier', args='--stdin'),
            Formatter('JSON', formatter=format_json),
            ExternalFormatter('Python', command='yapf'),
            ExternalFormatter('Rust', command='rustfmt'),
            ExternalFormatter('Swift', command='swiftformat'),
            ExternalFormatter('Terraform', command='terraform fmt', args='-'),
        ]

    def clear(self):
        self.formatters = []

    @property
    def all(self):
        return self.__formatters

    def by(self, predicate):
        return filter(predicate, self.all)

    def by_view(self, view):
        source = view.scope_name(0).split(' ')[0].split('.')[1]
        return next(self.by(lambda f: source in f.sources), None)

    def by_name(self, name):
        return next(self.by(lambda f: f.name == name), None)
