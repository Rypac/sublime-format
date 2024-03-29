from __future__ import annotations

import os
import subprocess


def shell(
    args: list[str],
    input: str,
    cwd: str,
    timeout: int = 60,
) -> str:
    startupinfo = None
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

    try:
        completed_process = subprocess.run(
            args=args,
            input=input,
            capture_output=True,
            shell=False,
            cwd=cwd,
            timeout=timeout,
            check=True,
            text=True,
            env=os.environ,
            startupinfo=startupinfo,
        )
    except subprocess.CalledProcessError as error:
        message = str(error)
        if stderr := error.stderr:
            message += f"\n${stderr}"
        elif stdout := error.stdout:
            message += f"\n${stdout}"
        raise Exception(message)

    return completed_process.stdout
