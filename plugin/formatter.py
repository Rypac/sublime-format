from __future__ import annotations

from sublime import expand_variables, score_selector
from sublime import Edit, Region, View

import os

from .settings import SettingsInterface
from .shell import shell
from .view import extract_variables


class Formatter:
    def __init__(self, name: str, settings: SettingsInterface):
        self._name = name
        self._settings = settings

    @property
    def name(self) -> str:
        return self._name

    @property
    def format_on_save(self) -> bool:
        return self._settings.format_on_save

    def score(self, scope: str) -> int:
        return (
            score_selector(scope, selector)
            if self._settings.enabled
            and (selector := self._settings.selector) is not None
            else -1
        )

    def format(self, view: View, edit: Edit, region: Region) -> None:
        text = view.substr(region)
        variables = extract_variables(view)
        args = [expand_variables(arg, variables) for arg in self._settings.cmd]

        cwd = (
            os.path.dirname(file_name)
            if (file_name := view.file_name())
            else next(iter(view.window().folders()), None)
        )

        formatted = shell(
            args=args,
            input=text,
            cwd=cwd,
            timeout=self._settings.timeout,
        )

        position = view.viewport_position()
        view.replace(edit, region, formatted)
        view.set_viewport_position(position, animate=False)
