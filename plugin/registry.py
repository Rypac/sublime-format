from __future__ import annotations

from sublime import score_selector, set_timeout_async, View, Window

from .formatter import Formatter
from .settings import (
    FormatSettings,
    MergedSettings,
    ProjectSettings,
    ViewSettings,
)


class FormatterRegistry:
    def __init__(self) -> None:
        self.settings = FormatSettings()
        self._window_registries: dict[int, WindowFormatterRegistry] = {}

    def startup(self) -> None:
        self.settings.add_on_change(
            "update_registry",
            lambda: set_timeout_async(self.update),
        )

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

        if (formatter_name := window_registry.lookup(scope)) is None:
            return None

        view_settings = ViewSettings(view)

        return Formatter(
            name=formatter_name,
            settings=MergedSettings(
                view_settings.formatter(formatter_name),
                self.settings.formatter(formatter_name),
                view_settings,
                self.settings,
            ),
        )


class WindowFormatterRegistry:
    def __init__(self, window: Window, settings: FormatSettings) -> None:
        self.window = window
        self.settings = settings
        self.project = ProjectSettings(window)
        self._enabled_in_settings = False
        self._enabled_in_project = False
        self._lookup_cache: dict[str, str] = {}

    def update(self) -> None:
        self._enabled_in_settings = self.settings.get("enabled", False)
        self._enabled_in_project = self.project.get("enabled", False)
        self._lookup_cache.clear()

    def lookup(self, scope: str) -> str | None:
        if scope in self._lookup_cache:
            return self._lookup_cache[scope]

        merged_formatters = {
            **self.settings.get("formatters", {}),
            **self.project.get("formatters", {}),
        }

        max_score: int = 0
        max_formatter: str | None = None
        for name, settings in merged_formatters.items():
            if (
                settings.get("enabled")
                or self._enabled_in_project
                or self._enabled_in_settings
            ):
                score = score_selector(scope, settings.get("selector"))
                if score > max_score:
                    max_score = score
                    max_formatter = name

        if max_score == 0:
            return None

        if max_formatter is not None and " " not in scope:
            self._lookup_cache[scope] = max_formatter

        return max_formatter
