from __future__ import annotations

from sublime import View, Window
from typing import Any, Dict, Optional

from .formatter import Formatter
from .settings import (
    FormatSettings,
    FormatterSettings,
    PluginSettings,
    ProjectFormatSettings,
    WindowFormatterSettings,
)
from .view import view_scope


class FormatterRegistry:
    def __init__(self) -> None:
        self._window_registries: Dict[int, WindowFormatterRegistry] = {}

    def startup(self) -> None:
        PluginSettings.load().add_on_change("reload_settings", self.update)
        self.update()

    def teardown(self) -> None:
        PluginSettings.load().clear_on_change("reload_settings")
        self._window_registries.clear()

    def register(self, window: Window) -> None:
        if not window.is_valid() or window.id() in self._window_registries:
            return

        window_registry = WindowFormatterRegistry(window)
        window_registry.update()
        self._window_registries[window.id()] = window_registry

    def unregister(self, window: Window) -> None:
        if (window_id := window.id()) in self._window_registries:
            del self._window_registries[window_id]

    def update(self) -> None:
        for window_registry in self._window_registries.values():
            window_registry.update()

    def update_window(self, window: Window) -> None:
        if window_registry := self._window_registries.get(window.id()):
            window_registry.update()

    def lookup(self, view: View, scope: str) -> Optional[Formatter]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if (window_registry := self._window_registries.get(window.id())) is None:
            return None

        return window_registry.lookup(scope)

    def settings(self) -> FormatSettings:
        return FormatSettings()

    def formatter_settings(self, name: str) -> FormatterSettings:
        return self.settings().formatter(name)


class WindowFormatterRegistry:
    def __init__(self, window: Window) -> None:
        self._window = window
        self._settings = FormatSettings()
        self._project_settings = ProjectFormatSettings(window)
        self._formatters: Dict[str, Formatter] = {}

    def update(self) -> None:
        formatters = self._settings.get("formatters", {}).keys()
        project_formatters = self._project_settings.get("formatters", {}).keys()
        latest_formatters = formatters | project_formatters

        current_formatters = self._formatters.keys()

        for formatter in latest_formatters - current_formatters:
            self._formatters[formatter] = Formatter(
                name=formatter,
                settings=WindowFormatterSettings(formatter, self._window),
            )

        for formatter in current_formatters - latest_formatters:
            del self._formatters[formatter]

    def lookup(self, scope: str) -> Optional[Formatter]:
        if not (formatters := self._formatters):
            return None

        formatter = max(formatters.values(), key=lambda f: f.score(scope))

        return formatter if formatter.score(scope) > 0 else None
