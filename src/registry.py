from .formatter import Formatter, JsonFormatter


class FormatterRegistry():
    def __init__(self):
        self.__formatters = []

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

    @property
    def all(self):
        return self.__formatters

    def by(self, predicate):
        return filter(predicate, self.all)

    def by_view(self, view):
        source = view.scope_name(0).split(' ')[0].split('.')[1]
        return next(self.by(lambda f: source in f.sources))

    def by_name(self, name):
        return next(self.by(lambda f: f.name == name))
