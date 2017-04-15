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

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return [file_name]

    def format(self, file=None, input=None):
        command = self.command()
        options = self.options
        args = self.file_args(file) if file else self.selection_args()
        return Command(command + options + args).run(input)


class ClangFormat(Formatter):
    def __init__(self):
        super().__init__(name='Clang', binary='clang-format')

    def file_args(self, file_name):
        return ['-i', file_name]


class ElmFormat(Formatter):
    def __init__(self):
        super().__init__(name='Elm', binary='elm-format')

    def selection_args(self):
        return ['--stdin']


class GoFormat(Formatter):
    def __init__(self):
        super().__init__(name='Go', binary='gofmt')

    def file_args(self, file_name):
        return ['-w', file_name]


class HaskellFormat(Formatter):
    def __init__(self):
        super().__init__(name='Haskell', binary='hindent')


class JavaScriptFormat(Formatter):
    def __init__(self):
        super().__init__(name='JavaScript', binary='prettier')

    def selection_args(self):
        return ['--stdin']

    def file_args(self, file_name):
        return ['--write', file_name]


class JsonFormat(Formatter):
    def __init__(self):
        super().__init__(name='JSON')

    def format(self, file=None, input=None):
        return self.format_file(file) if file else self.format_selection(input)

    def format_file(self, file):
        try:
            with open(file, 'r+') as handle:
                data = json.load(handle, object_pairs_hook=OrderedDict)
                handle.seek(0)
                json.dump(data, handle, indent=4)
                handle.truncate()
                return None, None
        except IOError as error:
            return None, error
        except ValueError:
            return None, 'Invalid JSON'

    def format_selection(self, selection):
        try:
            data = json.loads(selection, object_pairs_hook=OrderedDict)
            return json.dumps(data, indent=4), None
        except ValueError:
            return None, 'Invalid JSON'


class PythonFormat(Formatter):
    def __init__(self):
        super().__init__(name='Python', binary='yapf')

    def file_args(self, file_name):
        return ['--in-place', file_name]


class RustFormat(Formatter):
    def __init__(self):
        super().__init__(name='Rust', binary='rustfmt')

    def file_args(self, file_name):
        return ['--write-mode=overwrite', file_name]


class TerraformFormat(Formatter):
    def __init__(self):
        super().__init__(name='Terraform', binary='terraform')

    def command(self):
        return [self.binary, 'fmt']

    def selection_args(self):
        return ['-']
