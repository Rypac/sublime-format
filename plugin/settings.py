from __future__ import annotations

from contextlib import contextmanager
from sublime import Settings
from sublime import load_settings, save_settings
from typing import Any, Callable, Dict, List


class FormatSettings:
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

    def formatters(self) -> List[FormatterSettings]:
        return [self.formatter(name) for name in self.load().get("formatters", {})]

    def formatter(self, name: str) -> FormatterSettings:
        return FormatterSettings(name=name, settings=self)

    def enabled(self) -> bool:
        return self.get("enabled", default=True)

    def set_enabled(self, enabled: bool) -> None:
        self.set("enabled", enabled)

    def format_on_save(self) -> bool:
        return self.get("format_on_save", default=False)

    def set_format_on_save(self, enabled: bool) -> None:
        self.set("format_on_save", enabled)

    def timeout(self) -> int:
        return self.get("timeout", default=60)

    def get(self, key: str, default: Any = None) -> Any:
        return self.load().get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self.edit() as settings:
            settings[key] = value


class FormatterSettings:
    def __init__(self, name: str, settings: FormatSettings) -> None:
        self._name = name
        self._settings = settings

    def to_dict(self) -> Dict[str, Any]:
        settings = self._settings.to_dict()
        return {
            **{key: value for key, value in settings.items() if key != "formatters"},
            **settings.get("formatters", {}).get(self._name, {}),
        }

    @property
    def name(self) -> str:
        return self._name

    def selector(self) -> str:
        return self.get("selector")

    def cmd(self) -> List[str]:
        return self.get("cmd")

    def enabled(self) -> bool:
        return self.get("enabled")

    def set_enabled(self, enabled: bool) -> None:
        self.set("enabled", enabled)

    def format_on_save(self) -> bool:
        return self.get("format_on_save")

    def set_format_on_save(self, enabled: bool) -> None:
        self.set("format_on_save", enabled)

    def timeout(self) -> int:
        return self.get("timeout")

    def get(self, key: str, default: Any = None) -> Any:
        settings = self._settings.load()
        value = settings.get("formatters", {}).get(self.name, {}).get(key)
        return value if value is not None else settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self.edit() as settings:
            formatters = settings.setdefault("formatters", {})
            formatter_settings = formatters.setdefault(self.name, {})
            formatter_settings[key] = value
            settings["formatters"] = formatters
