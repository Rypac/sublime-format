from .formatter import Formatter, JsonFormatter


class FormatterRegistry():
    def __init__(self):
        self.__formatters = []
        self.__formatter_source_map = {}

    def populate(self):
        self.__formatters = [
            Formatter('Clang', command='clang-format'),
            Formatter('Elm', command='elm-format', args='--stdin'),
            Formatter('Go', command='gofmt'),
            Formatter('Haskell', command='hindent'),
            Formatter('JavaScript', command='prettier', args='--stdin'),
            Formatter('Python', command='yapf'),
            Formatter('Rust', command='rustfmt'),
            Formatter('Terraform', command='terraform fmt', args='-'),
            JsonFormatter(),
        ]
        self.__formatter_source_map = dict((source, formatter)
                                           for formatter in self.__formatters
                                           for source in formatter.sources)

    @property
    def all(self):
        return self.__formatters

    def by_view(self, view):
        source = view.scope_name(0).split(' ')[0].split('.')[1]
        return self.__formatter_source_map.get(source)

    def by_name(self, name):
        return next((x for x in self.all if x.name == name))
