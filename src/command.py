import subprocess
import os
from .settings import Settings


class Command():
    def __init__(self, command):
        self.__command = command
        self.__startup_info = None
        self.__shell = False
        if os.name == 'nt':
            self.__startup_info = subprocess.STARTUPINFO()
            self.__startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.__startup_info.wShowWindow = subprocess.SW_HIDE
            self.__shell = True

    @staticmethod
    def env(self):
        path = os.pathsep.join(Settings.paths())
        env = os.environ.copy()
        env['PATH'] = path + os.pathsep + env['PATH']
        return env

    def run(self, input):
        return subprocess.Popen(
            self.__command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=self.__startup_info,
            shell=self.__shell,
            env=self.env(),
            universal_newlines=True).communicate(input=input)
