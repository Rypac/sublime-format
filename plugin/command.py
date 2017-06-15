import subprocess
import os
from .settings import Settings


def env():
    path = os.pathsep.join(Settings.paths())
    env = os.environ.copy()
    env['PATH'] = path + os.pathsep + env['PATH']
    return env


def shell(command):
    startup_info = None
    shell = False
    if os.name == 'nt':
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup_info.wShowWindow = subprocess.SW_HIDE
        shell = True

    def run(input, *args, **kwargs):
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startup_info,
            shell=shell,
            env=env(),
            universal_newlines=True)
        stdout, stderr = process.communicate(input=input)
        ok = process.returncode == 0
        return ok, stdout, stderr

    return run
