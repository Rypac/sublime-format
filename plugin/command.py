import subprocess
import os


def shell(command, paths=[]):
    startup_info = None
    if os.name == 'nt':
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup_info.wShowWindow = subprocess.SW_HIDE

    env = os.environ.copy()
    if paths:
        env['PATH'] = os.pathsep.join(paths) + os.pathsep + env['PATH']

    def run(input, *args, **kwargs):
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startup_info,
            env=env,
            shell=False,
            universal_newlines=True)
        stdout, stderr = process.communicate(input=input)
        ok = process.returncode == 0
        return ok, stdout, stderr

    return run
