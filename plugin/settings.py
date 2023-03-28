from __future__ import annotations

from sublime import Settings
from sublime import load_settings, save_settings
from typing import Any, Callable, Dict, Optional

from .configuration import Configuration


class FormatterSettings:
    def __init__(self) -> None:
        self._settings_name = "Format.sublime-settings"

    def load(self) -> Settings:
        return load_settings(self._settings_name)

    def save(self) -> None:
        save_settings(self._settings_name)

    def to_dict(self) -> Dict[str, Any]:
        return self.load().to_dict()

    def add_on_change(self, tag: str, callback: Callable[[], None]) -> None:
        self.load().add_on_change(tag, callback)

    def clear_on_change(self, tag: str) -> None:
        self.load().clear_on_change(tag)

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

    def enabled(self, formatter: Optional[str] = None) -> bool:
        return self.get("enabled", formatter, default=True)

    def set_enabled(self, enabled: bool, formatter: Optional[str] = None) -> None:
        self.set("enabled", enabled, formatter)

    def format_on_save(self, formatter: Optional[str] = None) -> bool:
        return self.get("format_on_save", formatter, default=False)

    def set_format_on_save(
        self,
        enabled: bool,
        formatter: Optional[str] = None,
    ) -> None:
        self.set("format_on_save", enabled, formatter)

    def get(
        self,
        key: str,
        formatter: Optional[str] = None,
        default: Any = None,
    ) -> Optional[Any]:
        settings = self.load()
        return (
            settings.get("formatters", {}).get(formatter, {}).get(key, default)
            if formatter is not None
            else settings.get(key, default)
        )

    def set(self, key: str, value: Any, formatter: Optional[str] = None) -> None:
        settings = self.load()
        if formatter:
            formatters = settings.setdefault("formatters", {})
            formatter_settings = formatters.setdefault(formatter, {})
            formatter_settings[key] = value
            settings["formatters"] = formatters
        else:
            settings[key] = value
        self.save()
