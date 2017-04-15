import json
from collections import OrderedDict
from functools import wraps
from .cache import cache, recache
from .command import Command
from .settings import FormatterSettings


def formatter(name, command='', args=''):
    def decorator(cls):
        @wraps(cls)
        def make_formatter(*args, **kwargs):
            return cls(name, command, args, *args, **kwargs)
        return make_formatter
    return decorator


class Formatter():
    def __init__(self, name, command='', args=''):
        self.__name = name
        self.__command = command.split(' ') if command else []
        self.__args = args.split(' ') if args else []
        self.__settings = FormatterSettings(name.lower())

    @property
    def name(self):
        return self.__name

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

    def format(self, input):
        command = self.__command
        options = self.options
        args = self.__args
        return Command(command + options + args).run(input)


@formatter(name='Clang', command='clang-format')
class ClangFormat(Formatter):
    pass


@formatter(name='Elm', command='elm-format', args='--stdin')
class ElmFormat(Formatter):
    pass


@formatter(name='Go', command='gofmt')
class GoFormat(Formatter):
    pass


@formatter(name='Haskell', command='hindent')
class HaskellFormat(Formatter):
    pass


@formatter(name='JavaScript', command='prettier', args='--stdin')
class JavaScriptFormat(Formatter):
    pass


@formatter(name='JSON')
class JsonFormat(Formatter):
    def format(self, input):
        try:
            data = json.loads(input, object_pairs_hook=OrderedDict)
            return json.dumps(data, indent=4), None
        except ValueError:
            return None, 'Invalid JSON'


@formatter(name='Python', command='yapf')
class PythonFormat(Formatter):
    pass


@formatter(name='Rust', command='rustfmt')
class RustFormat(Formatter):
    pass


@formatter(name='Terraform', command='terraform fmt', args='-')
class TerraformFormat(Formatter):
    pass
