from __future__ import annotations

from sublime import score_selector, View

from .formatter import Formatter
from .settings import (
    CachedSettings,
    FormatSettings,
    MergedSettings,
    TopLevelSettings,
    ViewSettings,
)


class FormatterRegistry:
    def __init__(self) -> None:
        self.settings = FormatSettings()
        self._view_registries: dict[int, ScopedFormatterRegistry] = {}

    def startup(self) -> None:
        self.settings.add_on_change("update_registry", self.update)

    def teardown(self) -> None:
        self.settings.clear_on_change("update_registry")
        self._view_registries.clear()

    def register(self, view: View) -> None:
        if (view_id := view.id()) not in self._view_registries:
            self._view_registries[view_id] = ScopedFormatterRegistry(
                settings=self.settings,
                scoped_settings=ViewSettings(view),
            )

    def unregister(self, view: View) -> None:
        if (view_id := view.id()) in self._view_registries:
            del self._view_registries[view_id]

    def update(self, view: View | None = None) -> None:
        if view is not None:
            if view_registry := self._view_registries.get(view.id()):
                view_registry.update()
        else:
            for view_registry in self._view_registries.values():
                view_registry.update()

    def lookup(self, view: View, scope: str) -> Formatter | None:
        return (
            registry.lookup(scope)
            if (registry := self._view_registries.get(view.id())) is not None
            else None
        )


class ScopedFormatterRegistry:
    __slots__ = ["settings", "scoped_settings", "_lookup_cache"]

    def __init__(
        self,
        settings: TopLevelSettings,
        scoped_settings: TopLevelSettings,
    ) -> None:
        self.settings = settings
        self.scoped_settings = scoped_settings
        self._lookup_cache: dict[str, Formatter] = {}

    def update(self) -> None:
        for formatter in self._lookup_cache.values():
            formatter.settings.invalidate()

        self._lookup_cache.clear()

    def lookup(self, scope: str) -> Formatter | None:
        if scope in self._lookup_cache:
            return self._lookup_cache[scope]

        merged_formatters = {
            **self.settings.get("formatters", {}),
            **self.scoped_settings.get("formatters", {}),
        }

        if not merged_formatters:
            return None

        max_score: int = 0
        matched_formatter: str | None = None
        for name, settings in merged_formatters.items():
            if (selector := settings.get("selector")) is None:
                continue

            score = score_selector(scope, selector)
            if score > max_score:
                max_score = score
                matched_formatter = name

        if matched_formatter is None:
            return None

        formatter = Formatter(
            name=matched_formatter,
            settings=CachedSettings(
                MergedSettings(
                    self.scoped_settings.formatter(matched_formatter),
                    self.settings.formatter(matched_formatter),
                ),
            ),
        )

        if " " not in scope:
            self._lookup_cache[scope] = formatter

        return formatter
