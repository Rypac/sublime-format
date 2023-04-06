from __future__ import annotations

from enum import Enum
from sublime import load_settings, save_settings, Window
from typing import Any, Callable, Protocol

from .error import ErrorStyle


class Setting(Enum):
    SELECTOR = "selector"
    CMD = "cmd"
    ENABLED = "enabled"
    FORMAT_ON_SAVE = "format_on_save"
    ERROR_STYLE = "error_style"
    TIMEOUT = "timeout"


class Settings(Protocol):
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from settings for the given key, with an optional default."""
        ...

    def set(self, key: str, value: Any) -> None:
        """Stores a value in settings for the given key."""
        ...

    @property
    def selector(self) -> str:
        return self.get(Setting.SELECTOR.value)

    @property
    def cmd(self) -> list[str]:
        return self.get(Setting.CMD.value)

    @property
    def enabled(self) -> bool:
        return self.get(Setting.ENABLED.value)

    def set_enabled(self, enabled: bool) -> None:
        return self.set(Setting.ENABLED.value, enabled)

    @property
    def format_on_save(self) -> bool:
        return self.get(Setting.FORMAT_ON_SAVE.value)

    def set_format_on_save(self, enabled: bool) -> None:
        return self.set(Setting.FORMAT_ON_SAVE.value, enabled)

    @property
    def error_style(self) -> ErrorStyle:
        value = self.get(Setting.ERROR_STYLE.value)
        return next((style for style in ErrorStyle if style.value == value))

    @property
    def timeout(self) -> int:
        return self.get(Setting.TIMEOUT.value)


class FormatSettings(Settings):
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

    def formatters(self) -> list[FormatterSettings]:
        return [self.formatter(name) for name in self.get("formatters", {})]

    def formatter(self, name: str) -> FormatterSettings:
        return FormatterSettings(name, settings=self)


class FormatterSettings(Settings):
    def __init__(self, name: str, settings: FormatSettings) -> None:
        self.name = name
        self._settings = settings

    def get(self, key: str, default: Any = None) -> Any:
        value = self._settings.get("formatters", {}).get(self.name, {}).get(key)
        return value if value is not None else self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        formatters = self._settings.get("formatters", {})
        formatter = formatters.setdefault(self.name, {})
        formatter[key] = value
        self._settings.set("formatters", formatters)


class ProjectFormatSettings(Settings):
    def __init__(self, window: Window, settings: Settings) -> None:
        self._window = window
        self._settings = settings

    def get(self, key: str, default: Any = None) -> Any:
        project = self._window.project_data() or {}
        value = project.get("settings", {}).get("Format", {}).get(key)
        return value if value is not None else self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        project = self._window.project_data() or {}
        settings = project.setdefault("settings", {}).setdefault("Format", {})
        settings[key] = value
        self._window.set_project_data(project)

    def formatters(self) -> list[ProjectFormatterSettings]:
        return [self.formatter(name) for name in self.get("formatters", {})]

    def formatter(self, name: str) -> ProjectFormatterSettings:
        return ProjectFormatterSettings(name, project=self)


class ProjectFormatterSettings(Settings):
    def __init__(self, name: str, project: ProjectFormatSettings) -> None:
        self.name = name
        self._project = project

    def get(self, key: str, default: Any = None) -> Any:
        value = self._project.get("formatters", {}).get(self.name, {}).get(key)
        return value if value is not None else self._project.get(key, default)

    def set(self, key: str, value: Any) -> None:
        formatters = self._project.get("formatters", {})
        formatter = formatters.setdefault(self.name, {})
        formatter[key] = value
        self._project.set("formatters", formatters)
