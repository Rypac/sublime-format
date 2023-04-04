from __future__ import annotations

from sublime import View, Window
from typing import Any, Dict, Optional

from .formatter import Formatter
from .settings import (
    FormatSettings,
    FormatterSettings,
    ProjectFormatSettings,
    Setting,
    Settings,
)


class FormatterRegistry:
    def __init__(self) -> None:
        self._settings = FormatSettings()
        self._window_registries: Dict[int, WindowFormatterRegistry] = {}

    def startup(self) -> None:
        self._settings.add_on_change("reload_settings", self.update)
        self.update()

    def teardown(self) -> None:
        self._settings.clear_on_change("reload_settings")
        self._window_registries.clear()

    def register(self, window: Window) -> None:
        if not window.is_valid() or window.id() in self._window_registries:
            return

        window_registry = WindowFormatterRegistry(window, self._settings)
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
        return self._settings

    def formatter_settings(self, name: str) -> FormatterSettings:
        return self._settings.formatter(name)


class WindowFormatterRegistry:
    def __init__(self, window: Window, settings: FormatSettings) -> None:
        self._window = window
        self._settings = settings
        self._project = ProjectFormatSettings(window, settings)
        self._formatters: Dict[str, Formatter] = {}

    def update(self) -> None:
        formatters = self._settings.get("formatters", {}).keys()
        project_formatters = self._project.get("formatters", {}).keys()
        latest_formatters = formatters | project_formatters

        current_formatters = self._formatters.keys()

        for formatter in latest_formatters | current_formatters:
            if formatter not in current_formatters:
                project = ProjectFormatSettings(
                    window=self._window,
                    settings=self._settings.formatter(name=formatter),
                )

                self._formatters[formatter] = Formatter(
                    name=formatter,
                    settings=CachedSettings(settings=project.formatter(name=formatter)),
                )
            elif formatter not in latest_formatters:
                del self._formatters[formatter]
            else:
                self._formatters[formatter].settings.reload()

    def lookup(self, scope: str) -> Optional[Formatter]:
        if not (formatters := self._formatters):
            return None

        formatter = max(formatters.values(), key=lambda f: f.score(scope))

        return formatter if formatter.score(scope) > 0 else None


class CachedSettings(Settings):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._cached_settings = {
            setting.key: settings.get(*setting.value) for setting in Setting
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self._cached_settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings.set(key, value)
        self.reload()

    def reload(self) -> None:
        self._cached_settings.update(
            {setting.key: self._settings.get(*setting.value) for setting in Setting}
        )
