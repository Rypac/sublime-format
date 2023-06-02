from __future__ import annotations

from sublime import score_selector, View

from .formatter import Formatter
from .settings import CachedSettings, FormatSettings, MergedSettings, ViewSettings


class FormatterRegistry:
    def __init__(self) -> None:
        self.settings = FormatSettings()
        self._cache: dict[int, Formatter] = {}

    def startup(self) -> None:
        self.settings.add_on_change("update_registry", self.update)

    def teardown(self) -> None:
        self.settings.clear_on_change("update_registry")
        self._cache.clear()

    def unregister(self, view: View) -> None:
        if (view_id := view.id()) in self._cache:
            del self._cache[view_id]

    def update(self, window: Window | None = None) -> None:
        if window is not None:
            for view in window.views():
                self.unregister(view)
        else:
            self._cache.clear()

    def lookup(self, view: View, scope: str) -> Formatter | None:
        view_id = view.id()
        is_view_scope = " " not in scope

        if is_view_scope and (formatter := self._cache.get(view_id)):
            if score_selector(scope, formatter.settings.selector) > 0:
                return formatter
            else:
                del self._cache[view_id]

        view_settings = ViewSettings(view)
        merged_formatters = {
            **self.settings.get("formatters", {}),
            **view_settings.get("formatters", {}),
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
                    view_settings.formatter(matched_formatter),
                    self.settings.formatter(matched_formatter),
                ),
            ),
        )

        if is_view_scope:
            self._cache[view_id] = formatter

        return formatter
