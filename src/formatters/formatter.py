import subprocess
import os
from ..settings import Settings


def process_startup_info():
    if not os.name == 'nt':
        return None
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    return startupinfo


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
        return self.settings.get('binary', self.__binary)

    @property
    def format_on_save(self):
        return self.settings.get('format_on_save', False)

    @format_on_save.setter
    def format_on_save(self, value):
        self.settings.set('format_on_save', value)

    def command(self):
        return [self.binary]

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return [file_name]

    def format(self, file=None, input=None):
        args = self.file_args(file) if file else self.selection_args()
        return subprocess.Popen(
            self.command() + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=process_startup_info(),
            universal_newlines=True).communicate(input=input)
