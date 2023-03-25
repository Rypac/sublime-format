from __future__ import annotations

from sublime import Settings

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
    def selector(self) -> str:
        return self._config.selector

    @property
    def enabled(self) -> bool:
        return self._config.enabled

    @property
    def format_on_save(self) -> bool:
        return self._config.format_on_save

    def format(self, input: str, settings: Settings) -> None:
        shell(args=self._config.cmd, input=input, timeout=self._config.timeout)
