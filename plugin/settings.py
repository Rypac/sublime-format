from __future__ import annotations

from typing import Any, Callable, Protocol

from sublime import View, load_settings, save_settings

from .error import ErrorStyle


class Settings(Protocol):
    def get(self, key: str, default: Any = None) -> Any: ...

    def set(self, key: str, value: Any) -> None: ...

    @property
    def selector(self) -> str:
        return self.get("selector")

    @property
    def command(self) -> list[str]:
        return self.get("command")

    @property
    def enabled(self) -> bool:
        return self.get("enabled")

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        return self.set("enabled", enabled)

    @property
    def format_on_save(self) -> bool:
        return self.get("format_on_save")

    @format_on_save.setter
    def format_on_save(self, enabled: bool) -> None:
        return self.set("format_on_save", enabled)

    @property
    def error_style(self) -> ErrorStyle:
        value = self.get("error_style")
        return next(
            (style for style in ErrorStyle if style.value == value),
            ErrorStyle.PANEL,
        )

    @property
    def timeout(self) -> int:
        return self.get("timeout")


class TopLevelSettings(Settings, Protocol):
    def formatters(self) -> dict[str, Settings]:
        return {name: self.formatter(name) for name in self.get("formatters", {})}

    def formatter(self, name: str) -> Settings:
        return MergedSettings(FormatterSettings(name, settings=self), self)

    def selectors(self) -> dict[str, str]:
        return {
            name: selector
            for name, settings in self.get("formatters", {}).items()
            if (selector := settings.get("selector")) is not None
        }


class FormatSettings(TopLevelSettings):
    def __init__(self) -> None:
        self._sublime_settings = load_settings("Format.sublime-settings")

    def get(self, key: str, default: Any = None) -> Any:
        return self._sublime_settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._sublime_settings[key] = value
        save_settings("Format.sublime-settings")

    def add_on_change(self, key: str, listener: Callable[[], None]) -> None:
        self._sublime_settings.add_on_change(key, listener)

    def clear_on_change(self, key: str) -> None:
        self._sublime_settings.clear_on_change(key)


class ViewSettings(TopLevelSettings):
    __slots__ = ["view"]

    def __init__(self, view: View) -> None:
        self.view = view

    def get(self, key: str, default: Any = None) -> Any:
        return self.view.settings().get("Format", {}).get(key, default)

    def set(self, key: str, value: Any) -> None:
        settings = self.view.settings().setdefault("Format", {})
        settings[key] = value
        self.view.settings()["Format"] = settings


class FormatterSettings(Settings):
    __slots__ = ["name", "settings"]

    def __init__(self, name: str, settings: TopLevelSettings) -> None:
        self.name = name
        self.settings = settings

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get("formatters", {}).get(self.name, {}).get(key, default)

    def set(self, key: str, value: Any) -> None:
        formatters = self.settings.get("formatters", {})
        formatter = formatters.setdefault(self.name, {})
        formatter[key] = value
        self.settings.set("formatters", formatters)


class MergedSettings(Settings):
    __slots__ = ["all"]

    def __init__(self, *args: Settings) -> None:
        self.all = args

    def get(self, key: str, default: Any = None) -> Any:
        return next(
            (value for source in self.all if (value := source.get(key)) is not None),
            default,
        )

    def set(self, key: str, value: Any) -> None:
        if source := next(iter(self.all), None):
            source.set(key, value)
