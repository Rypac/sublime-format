from __future__ import annotations

from sublime import expand_variables
from sublime import Edit, Region, View

import os

from .error import FormatError
from .settings import Settings
from .shell import shell
from .view import extract_variables


class Formatter:
    __slots__ = ["name", "selector", "settings"]

    def __init__(self, name: str, selector: str, settings: Settings):
        self.name: str = name
        self.selector: str = selector
        self.settings: Settings = settings

    def format(self, view: View, edit: Edit, region: Region) -> None:
        text = view.substr(region)
        variables = extract_variables(view)
        command = [expand_variables(arg, variables) for arg in self.settings.command]

        cwd = (
            os.path.dirname(file_name)
            if (file_name := view.file_name())
            else next(iter(view.window().folders()), None)
        )

        try:
            formatted = shell(
                args=command,
                input=text,
                cwd=cwd,
                timeout=self.settings.timeout,
            )
        except Exception as err:
            raise FormatError(message=str(err), style=self.settings.error_style)

        position = view.viewport_position()
        view.replace(edit, region, formatted)
        view.set_viewport_position(position, animate=False)
