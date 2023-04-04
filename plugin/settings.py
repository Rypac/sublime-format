from __future__ import annotations

from enum import Enum
from sublime import load_settings, save_settings, Window
from typing import Any, Callable, List, Optional, Protocol


class Setting(Enum):
    SELECTOR = "selector", None
    CMD = "cmd", None
    ENABLED = "enabled", True
    FORMAT_ON_SAVE = "format_on_save", False
    ERROR_STYLE = "error_style", "panel"
    TIMEOUT = "timeout", 60

    def __init__(self, key: str, default: Any):
        self.key = key
        self.default = default


class Settings(Protocol):
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from settings for the given key, with an optional default."""
        ...

    def set(self, key: str, value: Any) -> None:
        """Stores a value in settings for the given key."""
        ...

    @property
    def selector(self) -> str:
        return self.get(*Setting.SELECTOR.value)

    @property
    def cmd(self) -> List[str]:
        return self.get(*Setting.CMD.value)

    @property
    def enabled(self) -> bool:
        return self.get(*Setting.ENABLED.value)

    def set_enabled(self, enabled: bool) -> None:
        return self.set(Setting.ENABLED.key, enabled)

    @property
    def format_on_save(self) -> bool:
        return self.get(*Setting.FORMAT_ON_SAVE.value)

    def set_format_on_save(self, enabled: bool) -> None:
        return self.set(Setting.FORMAT_ON_SAVE.key, enabled)

    @property
    def error_style(self) -> str:
        return self.get(*Setting.ERROR_STYLE.value)

    @property
    def timeout(self) -> int:
        return self.get(*Setting.TIMEOUT.value)


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

    def formatters(self) -> List[FormatterSettings]:
        return [
            FormatterSettings(name, settings=self)
            for name in self.get("formatters", {})
        ]

    def formatter(self, name: str) -> Optional[FormatterSettings]:
        return (
            FormatterSettings(name, settings=self)
            if name in self.get("formatters", {})
            else None
        )


class FormatterSettings(Settings):
    def __init__(self, name: str, settings: FormatSettings) -> None:
        self._name = name
        self._settings = settings

    @property
    def name(self) -> str:
        return self._name

    def get(self, key: str, default: Any = None) -> Any:
        value = self._settings.get("formatters", {}).get(self._name, {}).get(key)
        return value if value is not None else self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        formatters = self._settings.get("formatters", {})
        formatter = formatters.setdefault(self._name, {})
        formatter[key] = value
        self._settings.set("formatters", formatters)


class ProjectFormatSettings(Settings):
    def __init__(self, window: Window) -> None:
        self._window = window

    def get(self, key: str, default: Any = None) -> Any:
        if not (project := self._window.project_data()):
            return default

        return project.get("settings", {}).get("Format", {}).get(key, default)

    def set(self, key: str, value: Any) -> None:
        project = self._window.project_data() or {}
        settings = project.setdefault("settings", {}).setdefault("Format", {})
        settings[key] = value
        self._window.set_project_data(project)

    def formatters(self) -> List[ProjectFormatterSettings]:
        return [
            ProjectFormatterSettings(name, project=self)
            for name in self.get("formatters", {})
        ]

    def formatter(self, name: str) -> Optional[ProjectFormatterSettings]:
        return (
            ProjectFormatterSettings(name, project=self)
            if name in self.get("formatters", {})
            else None
        )


class ProjectFormatterSettings(Settings):
    def __init__(self, name: str, project: ProjectFormatSettings) -> None:
        self._name = name
        self._project = project

    @property
    def name(self) -> str:
        return self._name

    def get(self, key: str, default: Any = None) -> Any:
        value = self._project.get("formatters", {}).get(self._name, {}).get(key)
        return value if value is not None else self._project.get(key, default)

    def set(self, key: str, value: Any) -> None:
        formatters = self._project.get("formatters", {})
        formatter = formatters.setdefault(self._name, {})
        formatter[key] = value
        self._project.set("formatters", formatters)
