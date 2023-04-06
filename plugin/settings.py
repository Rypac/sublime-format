from __future__ import annotations

from sublime import load_settings, save_settings, Window
from typing import Any, Callable, Protocol

from .error import ErrorStyle


class Settings(Protocol):
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from settings for the given key, with an optional default."""
        ...

    def set(self, key: str, value: Any) -> None:
        """Stores a value in settings for the given key."""
        ...

    @property
    def selector(self) -> str:
        return self.get("selector")

    @property
    def cmd(self) -> list[str]:
        return self.get("cmd")

    @property
    def enabled(self) -> bool:
        return self.get("enabled")

    def set_enabled(self, enabled: bool) -> None:
        return self.set("enabled", enabled)

    @property
    def format_on_save(self) -> bool:
        return self.get("format_on_save")

    def set_format_on_save(self, enabled: bool) -> None:
        return self.set("format_on_save", enabled)

    @property
    def error_style(self) -> ErrorStyle:
        value = self.get("error_style")
        return next((style for style in ErrorStyle if style.value == value))

    @property
    def timeout(self) -> int:
        return self.get("timeout")


class TopLevelSettings(Settings, Protocol):
    def formatters(self) -> dict[str, Settings]:
        return {name: self.formatter(name) for name in self.get("formatters", {})}

    def formatter(self, name: str) -> Settings:
        return MergedSettings(FormatterSettings(name, settings=self), self)


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


class ProjectSettings(TopLevelSettings):
    __slots__ = ["window"]

    def __init__(self, window: Window) -> None:
        self.window = window

    def get(self, key: str, default: Any = None) -> Any:
        project = self.window.project_data() or {}
        return project.get("settings", {}).get("Format", {}).get(key, default)

    def set(self, key: str, value: Any) -> None:
        project = self.window.project_data() or {}
        settings = project.setdefault("settings", {}).setdefault("Format", {})
        settings[key] = value
        self.window.set_project_data(project)


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
        if (source := next((source for source in self.all))) is not None:
            source.set(key, value)
