from __future__ import annotations

from sublime import expand_variables, score_selector
from sublime import Edit, Region, View

import os

from .error import FormatError
from .settings import Settings
from .shell import shell
from .view import extract_variables


class Formatter:
    def __init__(self, name: str, settings: Settings):
        self._name = name
        self._settings = settings

    @property
    def name(self) -> str:
        return self._name

    @property
    def settings(self) -> Settings:
        return self._settings

    def score(self, scope: str) -> int:
        return (
            score_selector(scope, selector)
            if self.settings.enabled
            and (selector := self.settings.selector) is not None
            else -1
        )

    def format(self, view: View, edit: Edit, region: Region) -> None:
        text = view.substr(region)
        variables = extract_variables(view)
        args = [expand_variables(arg, variables) for arg in self.settings.cmd]

        cwd = (
            os.path.dirname(file_name)
            if (file_name := view.file_name())
            else next(iter(view.window().folders()), None)
        )

        try:
            formatted = shell(
                args=args,
                input=text,
                cwd=cwd,
                timeout=self.settings.timeout,
            )
        except Exception as err:
            raise FormatError(message=str(err), style=self.settings.error_style)

        position = view.viewport_position()
        view.replace(edit, region, formatted)
        view.set_viewport_position(position, animate=False)
