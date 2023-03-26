from __future__ import annotations

from sublime import expand_variables, score_selector, Region, Settings, View

import os

from .configuration import Configuration
from .shell import shell


class Formatter:
    def __init__(self, name: str, config: Configuration):
        self._name = name
        self._config = config

    @property
    def name(self) -> str:
        return self._name

    @property
    def enabled(self) -> bool:
        return self._config.enabled

    @property
    def format_on_save(self) -> bool:
        return self._config.format_on_save

    def score(self, scope: str) -> int:
        return (
            score_selector(scope, selector)
            if (selector := self._config.selector) is not None
            else -1
        )

    def format(self, view: View, edit: Edit, region: Region) -> None:
        text = view.substr(region)
        variables = extract_variables(view)
        args = [expand_variables(arg, variables) for arg in self._config.cmd]

        formatted = shell(args=args, input=text, timeout=self._config.timeout)

        position = view.viewport_position()
        view.replace(edit, region, formatted)
        sublime.set_timeout(
            lambda: view.set_viewport_position(position, animate=False), 0
        )


def extract_variables(view: View) -> Dict[str, str]:
    settings = view.settings()
    tab_size = settings.get("tab_size") or 0
    indent = " " * tab_size if settings.get("translate_tabs_to_spaces") else "\t"

    vars = view.window().extract_variables()
    vars["tab_size"] = str(tab_size)
    vars["indent"] = indent
    vars.update(os.environ)

    return vars
