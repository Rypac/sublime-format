from __future__ import annotations

from sublime import expand_variables
from sublime import Edit, Region, View

import os
import subprocess

from .error import FormatError
from .settings import Settings


class Formatter:
    __slots__ = ["name", "selector", "settings"]

    def __init__(self, name: str, selector: str, settings: Settings):
        self.name: str = name
        self.selector: str = selector
        self.settings: Settings = settings

    def format(self, view: View, edit: Edit, region: Region) -> None:
        text = view.substr(region)
        variables = self._extract_variables(view)
        command = [expand_variables(arg, variables) for arg in self.settings.command]

        cwd = (
            os.path.dirname(file_name)
            if (file_name := view.file_name())
            else next(iter(view.window().folders()), None)
        )

        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        try:
            completed_process = subprocess.run(
                args=command,
                input=text,
                capture_output=True,
                shell=False,
                cwd=cwd,
                timeout=self.settings.timeout,
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

            raise FormatError(message=message, style=self.settings.error_style)

        position = view.viewport_position()
        view.replace(edit, region, completed_process.stdout)
        view.set_viewport_position(position, animate=False)

    def _extract_variables(self, view: View) -> dict[str, str]:
        settings = view.settings()
        tab_size = settings.get("tab_size") or 0
        indent = " " * tab_size if settings.get("translate_tabs_to_spaces") else "\t"

        variables = window.extract_variables() if (window := view.window()) else {}
        variables["tab_size"] = str(tab_size)
        variables["indent"] = indent
        variables.update(os.environ)

        return variables
