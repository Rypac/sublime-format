from __future__ import annotations

from sublime import Settings
from sublime import load_settings, save_settings
from typing import Any, Callable, Dict, Optional

from .configuration import Configuration


class FormatterSettings:
    def __init__(self, formatter_name: Optional[str] = None) -> None:
        self._settings_name = "Format.sublime-settings"
        self._formatter_name = formatter_name

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

    def formatter(self, name: str) -> FormatterSettings:
        return FormatterSettings(formatter_name = name)

    def enabled(self) -> bool:
        return self.get("enabled", default=True)

    def set_enabled(self, enabled: bool) -> None:
        self.set("enabled", enabled)

    def format_on_save(self) -> bool:
        return self.get("format_on_save", default=False)

    def set_format_on_save(self, enabled: bool) -> None:
        self.set("format_on_save", enabled)

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        settings = self.load()
        return (
            settings.get("formatters", {}).get(formatter, {}).get(key, default)
            if (formatter := self._formatter_name) is not None
            else settings.get(key, default)
        )

    def set(self, key: str, value: Any) -> None:
        settings = self.load()
        if (formatter := self._formatter_name) is not None:
            formatters = settings.setdefault("formatters", {})
            formatter_settings = formatters.setdefault(formatter, {})
            formatter_settings[key] = value
            settings["formatters"] = formatters
        else:
            settings[key] = value
        self.save()
