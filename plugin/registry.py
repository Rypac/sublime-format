from __future__ import annotations

from sublime import score_selector, View, Window

from .formatter import Formatter
from .settings import FormatSettings, MergedSettings, ViewSettings


class FormatterRegistry:
    def __init__(self) -> None:
        self.settings = FormatSettings()
        self._cache: dict[int, Formatter | str] = {}

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

        if is_view_scope and (formatter := self._cache.get(view_id)) is not None:
            if isinstance(formatter, Formatter):
                if score_selector(scope, formatter.selector) > 0:
                    return formatter
            elif isinstance(formatter, str):
                if scope == formatter:
                    return None

            del self._cache[view_id]

        view_settings = ViewSettings(view)

        formatter_selectors = {
            **self.settings.selectors(),
            **view_settings.selectors(),
        }

        max_score: int = 0
        matched_formatter: str | None = None
        for name, selector in formatter_selectors.items():
            if (score := score_selector(scope, selector)) > max_score:
                max_score = score
                matched_formatter = name

        formatter = (
            Formatter(
                name=matched_formatter,
                selector=formatter_selectors[matched_formatter],
                settings=MergedSettings(
                    view_settings.formatter(matched_formatter),
                    self.settings.formatter(matched_formatter),
                ),
            )
            if matched_formatter is not None
            else None
        )

        if is_view_scope:
            self._cache[view_id] = formatter or scope

        return formatter
