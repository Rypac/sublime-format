import json
from collections import OrderedDict
from .cache import cache, recache
from .command import Command
from .settings import FormatterSettings


def formatter(name, binary=None):
    def decorator(f):
        def make_formatter():
            return Formatter(name, binary)
        return make_formatter
    return decorator


class Formatter():
    def __init__(self, name, binary=None):
        self.__name = name
        self.__binary = binary
        self.__settings = FormatterSettings(name.lower())

    @property
    def name(self):
        return self.__name

    @property
    def binary(self):
        return self.__binary

    @property
    @cache
    def sources(self):
        return self.__settings.sources

    @property
    @cache
    def options(self):
        return self.__settings.args

    @property
    @cache
    def format_on_save(self):
        return self.__settings.format_on_save

    @format_on_save.setter
    @recache
    def format_on_save(self, value):
        self.__settings.format_on_save = value

    def command(self):
        return [self.binary]

    def args(self):
        return []

    def format(self, input):
        command = self.command()
        options = self.options
        args = self.args()
        return Command(command + options + args).run(input)


@formatter(name='Clang', binary='clang-format')
class ClangFormat(Formatter):
    pass


@formatter(name='Elm', binary='elm-format')
class ElmFormat(Formatter):
    def args(self):
        return ['--stdin']


@formatter(name='Go', binary='gofmt')
class GoFormat(Formatter):
    pass


@formatter(name='Haskell', binary='hindent')
class HaskellFormat(Formatter):
    pass


@formatter(name='JavaScript', binary='prettier')
class JavaScriptFormat(Formatter):
    def args(self):
        return ['--stdin']


@formatter(name='JSON')
class JsonFormat(Formatter):
    def format(self, input):
        try:
            data = json.loads(input, object_pairs_hook=OrderedDict)
            return json.dumps(data, indent=4), None
        except ValueError:
            return None, 'Invalid JSON'


@formatter(name='Python', binary='yapf')
class PythonFormat(Formatter):
    pass


@formatter(name='Rust', binary='rustfmt')
class RustFormat(Formatter):
    pass


@formatter(name='Terraform', binary='terraform')
class TerraformFormat(Formatter):
    def command(self):
        return [self.binary, 'fmt']

    def args(self):
        return ['-']
