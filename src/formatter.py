from .command import Command
from .settings import Settings


class Formatter(object):
    def __init__(self, name=None, source=None, binary=None):
        self.__name = name
        self.__source = 'source.' + (source if source else name.lower())
        self.__binary = binary
        self.__settings = Settings(name.lower())

    @property
    def settings(self):
        return self.__settings

    @property
    def name(self):
        return self.__name

    @property
    def source(self):
        return self.__source

    @property
    def binary(self):
        return self.settings.get('binary', default=self.__binary)

    @property
    def options(self):
        return self.settings.get('options', default={})

    @property
    def format_on_save(self):
        return self.settings.get('format_on_save', default=False)

    @format_on_save.setter
    def format_on_save(self, value):
        self.settings.set('format_on_save', value)

    def command(self):
        return [self.binary]

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return [file_name]

    def parsed_options(self):
        options = []
        for key, value in self.options.items():
            options.extend(['--' + key, value])
        return options

    def format(self, file=None, input=None):
        command = self.command()
        options = self.parsed_options()
        args = self.file_args(file) if file else self.selection_args()
        return Command(command + options + args).run(input)


class ClangFormat(Formatter):
    def __init__(self):
        super().__init__(name='Clang', source='c++', binary='clang-format')

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


class JavaScriptFormat(Formatter):
    def __init__(self):
        super().__init__(name='JavaScript', source='js', binary='prettier')

    def command(self):
        return [self.settings.get('node'), self.binary]

    def selection_args(self):
        return ['--stdin']

    def file_args(self, file_name):
        return ['--write', file_name]


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
