from __future__ import annotations

from sublime import expand_variables, score_selector, Region, View

from .configuration import Configuration
from .shell import shell
from .view import extract_variables


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
