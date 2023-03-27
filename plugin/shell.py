from __future__ import annotations

from typing import List

import os
import subprocess


def shell(args: List[str], input: str, cwd: str, paths: List[str] = [], timeout: int = 60) -> str:
    startupinfo = None
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

    env = os.environ.copy()
    if paths:
        env["PATH"] = os.pathsep.join(paths) + os.pathsep + env["PATH"]

    process = subprocess.Popen(
        args=args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=startupinfo,
        env=env,
        cwd=cwd,
        shell=False,
        text=True,
    )

    try:
        stdout, stderr = process.communicate(input=input, timeout=timeout)
    except TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()

    if process.returncode != 0:
        msg = str(subprocess.CalledProcessError(process.returncode, args))
        if len(stderr) > 0:
            msg += f"\n${stderr}"
        elif len(stdout) > 0:
            msg += f"\n${stdout}"
        raise Exception(msg)

    return stdout
