from __future__ import annotations

from sublime import score_selector, View, Window

from .formatter import Formatter
from .settings import CachedSettings, FormatSettings, MergedSettings, ViewSettings


class FormatterRegistry:
    def __init__(self) -> None:
        self.settings = FormatSettings()
        self._view_registries: dict[int, ViewFormatterRegistry] = {}

    def startup(self) -> None:
        self.settings.add_on_change("update_registry", self.update)

    def teardown(self) -> None:
        self.settings.clear_on_change("update_registry")
        self._view_registries.clear()

    def register(self, view: View) -> None:
        if (view_id := view.id()) not in self._view_registries:
            view_registry = ViewFormatterRegistry(view, self.settings)
            self._view_registries[view_id] = view_registry

    def unregister(self, view: View) -> None:
        if (view_id := view.id()) in self._view_registries:
            del self._view_registries[view_id]

    def update(self) -> None:
        for view_registry in self._view_registries.values():
            view_registry.update()

    def update_window(self, window: Window) -> None:
        for view in window.views():
            if view_registry := self._view_registries.get(view.id()):
                view_registry.update()

    def lookup(self, view: View, scope: str) -> Formatter | None:
        return (
            registry.lookup(scope)
            if (registry := self._view_registries.get(view.id())) is not None
            else None
        )


class ViewFormatterRegistry:
    def __init__(self, view: View, settings: FormatSettings) -> None:
        self.settings = settings
        self.view_settings = ViewSettings(view)
        self._lookup_cache: dict[str, Formatter] = {}

    def update(self) -> None:
        self._lookup_cache.clear()

    def lookup(self, scope: str) -> Formatter | None:
        if scope in self._lookup_cache:
            return self._lookup_cache[scope]

        merged_formatters = {
            **self.settings.get("formatters", {}),
            **self.view_settings.get("formatters", {}),
        }

        if not merged_formatters:
            return None

        enabled_in_view = self.view_settings.enabled
        enabled_in_settings = self.settings.enabled

        max_score: int = 0
        matched_formatter: str | None = None
        for name, settings in merged_formatters.items():
            if settings.get("enabled") or enabled_in_view or enabled_in_settings:
                score = score_selector(scope, settings.get("selector"))
                if score > max_score:
                    max_score = score
                    matched_formatter = name

        if max_score == 0 or matched_formatter is None:
            return None

        formatter = Formatter(
            name=matched_formatter,
            settings=CachedSettings(
                MergedSettings(
                    self.view_settings.formatter(matched_formatter),
                    self.settings.formatter(matched_formatter),
                    self.view_settings,
                    self.settings,
                ),
            ),
        )

        if " " not in scope:
            self._lookup_cache[scope] = formatter

        return formatter
