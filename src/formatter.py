import json
from collections import OrderedDict
from .cache import cache, recache
from .command import Command
from .settings import FormatterSettings


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


class ClangFormat(Formatter):
    def __init__(self):
        super().__init__(name='Clang', binary='clang-format')


class ElmFormat(Formatter):
    def __init__(self):
        super().__init__(name='Elm', binary='elm-format')

    def args(self):
        return ['--stdin']


class GoFormat(Formatter):
    def __init__(self):
        super().__init__(name='Go', binary='gofmt')


class HaskellFormat(Formatter):
    def __init__(self):
        super().__init__(name='Haskell', binary='hindent')


class JavaScriptFormat(Formatter):
    def __init__(self):
        super().__init__(name='JavaScript', binary='prettier')

    def args(self):
        return ['--stdin']


class JsonFormat(Formatter):
    def __init__(self):
        super().__init__(name='JSON')

    def format(self, input):
        try:
            data = json.loads(input, object_pairs_hook=OrderedDict)
            return json.dumps(data, indent=4), None
        except ValueError:
            return None, 'Invalid JSON'


class PythonFormat(Formatter):
    def __init__(self):
        super().__init__(name='Python', binary='yapf')


class RustFormat(Formatter):
    def __init__(self):
        super().__init__(name='Rust', binary='rustfmt')


class TerraformFormat(Formatter):
    def __init__(self):
        super().__init__(name='Terraform', binary='terraform')

    def command(self):
        return [self.binary, 'fmt']

    def args(self):
        return ['-']
