from __future__ import annotations

from sublime import View, Window
from typing import Any

from .cache import cached
from .formatter import Formatter
from .settings import (
    FormatSettings,
    FormatterSettings,
    MergedSettings,
    ProjectSettings,
    SettingKey,
    Settings,
)


class FormatterRegistry:
    def __init__(self) -> None:
        self.settings = FormatSettings()
        self._window_registries: dict[int, WindowFormatterRegistry] = {}

    def startup(self) -> None:
        self.settings.add_on_change("update_registry", self.update)

    def teardown(self) -> None:
        self.settings.clear_on_change("update_registry")
        self._window_registries.clear()

    def register(self, window: Window) -> None:
        if not window.is_valid() or window.id() in self._window_registries:
            return

        window_registry = WindowFormatterRegistry(window, self.settings)
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

    def lookup(self, view: View, scope: str) -> Formatter | None:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if (window_registry := self._window_registries.get(window.id())) is None:
            return None

        return window_registry.lookup(scope)


class WindowFormatterRegistry:
    def __init__(self, window: Window, settings: FormatSettings) -> None:
        self.window = window
        self.settings = settings
        self.project = ProjectSettings(window)
        self._formatters: dict[str, Formatter] = {}
        self.lookup_cache: dict[str, str] = {}

    def update(self) -> None:
        formatters = self.settings.get("formatters", {}).keys()
        project_formatters = self.project.get("formatters", {}).keys()
        latest_formatters = formatters | project_formatters

        current_formatters = self._formatters.keys()

        for formatter in latest_formatters | current_formatters:
            if formatter not in current_formatters:
                self._formatters[formatter] = Formatter(
                    name=formatter,
                    settings=CachedSettings(
                        MergedSettings(
                            FormatterSettings(formatter, self.project),
                            FormatterSettings(formatter, self.settings),
                            self.project,
                            self.settings,
                        ),
                    ),
                )
            elif formatter not in latest_formatters:
                del self._formatters[formatter]
            else:
                self._formatters[formatter].settings.invalidate()

        self.lookup_cache.clear()

    @cached(
        cache=lambda self: self.lookup_cache,
        key=lambda scope: scope,
        include=lambda scope, _: " " not in scope,
    )
    def lookup(self, scope: str) -> Formatter | None:
        if not (formatters := self._formatters):
            return None

        formatter = max(formatters.values(), key=lambda f: f.score(scope))

        return formatter if formatter.score(scope) > 0 else None


class CachedSettings(Settings):
    __slots__ = ["_settings", "_cached_settings"]

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._cached_settings: dict[str, Any] = {}

    @cached(
        cache=lambda self: self._cached_settings,
        key=lambda key: key,
    )
    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._settings.set(key, value)
        del self._cached_settings[key]

    def invalidate(self) -> None:
        self._cached_settings.clear()
