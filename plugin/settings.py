from __future__ import annotations

from contextlib import contextmanager
from sublime import Settings
from sublime import load_settings, save_settings
from typing import Any, Callable, Dict, Optional

from .configuration import Configuration


class FormatterSettings:
    def __init__(self) -> None:
        self._settings_name = "Format.sublime-settings"

    def load(self) -> Settings:
        return load_settings(self._settings_name)

    @contextmanager
    def edit(self) -> Settings:
        settings = self.load()
        yield settings
        save_settings(self._settings_name)

    def to_dict(self) -> Dict[str, Any]:
        return self.load().to_dict()

    def add_on_change(self, tag: str, callback: Callable[[], None]) -> None:
        self.load().add_on_change(tag, callback)

    def clear_on_change(self, tag: str) -> None:
        self.load().clear_on_change(tag)

    def is_enabled(self, name: Optional[str] = None) -> bool:
        return self.get("enabled", formatter=name, default=True)

    def all_enabled(self) -> List[str]:
        return (
            name
            for name, settings in self.load().get("formatters", {}).items()
            if settings.get("enabled", False)
        )

    def all_disabled(self) -> List[str]:
        return (
            name
            for name, settings in self.load().get("formatters", {}).items()
            if not settings.get("enabled", False)
        )

    def enable(self, name: Optional[str] = None) -> None:
        self._set_enabled(name, True)

    def disable(self, name: Optional[str] = None) -> None:
        self._set_enabled(name, False)

    def _set_enabled(self, name: Optional[str], is_enabled: bool) -> None:
        with self.edit() as settings:
            if name:
                formatters = settings.get("formatters", {})
                formatter = formatters.setdefault(name, {})
                formatter["enabled"] = is_enabled
                settings["formatters"] = formatters
            else:
                settings["enabled"] = is_enabled

    def is_format_on_save_enabled(self, name: Optional[str] = None) -> bool:
        return self.get("format_on_save", formatter=name, default=False)

    def enable_format_on_save(self, name: Optional[str] = None) -> None:
        self._set_format_on_save_enabled(name, True)

    def disable_format_on_save(self, name: Optional[str] = None) -> None:
        self._set_format_on_save_enabled(name, False)

    def _set_format_on_save_enabled(
        self,
        name: Optional[str],
        is_enabled: bool,
    ) -> None:
        with self.edit() as settings:
            if name:
                formatters = settings.get("formatters", {})
                formatter = formatters.setdefault(name, {})
                formatter["format_on_save"] = is_enabled
                settings["formatters"] = formatters
            else:
                settings["format_on_save"] = is_enabled

    def get(
        self,
        key: str,
        formatter: Optional[str] = None,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        if not formatter:
            return self.load().get(key, default)
        return self.load().get("formatters", {}).get(formatter, {}).get(key, default)
