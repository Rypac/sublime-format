import subprocess
import os
from .settings import Settings


class ShellCommand:
    def __init__(self, args):
        self.__args = args
        self.__startup_info = None
        self.__shell = False
        if os.name == 'nt':
            self.__startup_info = subprocess.STARTUPINFO()
            self.__startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.__startup_info.wShowWindow = subprocess.SW_HIDE
            self.__shell = True

    @property
    def args(self):
        return self.__args

    @staticmethod
    def env():
        path = os.pathsep.join(Settings.paths())
        env = os.environ.copy()
        env['PATH'] = path + os.pathsep + env['PATH']
        return env

    def run(self, input):
        return subprocess.Popen(
            self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=self.__startup_info,
            shell=self.__shell,
            env=self.env(),
            universal_newlines=True).communicate(input=input)
