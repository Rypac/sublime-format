from __future__ import annotations

from enum import Enum
from sublime import load_settings, save_settings, Settings, Window
from typing import Any, Callable, Dict, List, Optional, Protocol


class PluginSettings:
    @staticmethod
    def load() -> Settings:
        return load_settings("Format.sublime-settings")

    @staticmethod
    def save() -> None:
        save_settings("Format.sublime-settings")


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


class SettingsInterface(Protocol):
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


class FormatSettings(SettingsInterface):
    def get(self, key: str, default: Any = None) -> Any:
        return PluginSettings.load().get(key, default)

    def set(self, key: str, value: Any) -> None:
        settings = PluginSettings.load()
        settings[key] = value
        PluginSettings.save()

    def formatters(self) -> List[FormatterSettings]:
        return [FormatterSettings(name) for name in self.get("formatters", {})]

    def formatter(self, name: str) -> Optional[FormatterSettings]:
        return FormatterSettings(name) if name in self.get("formatters", {}) else None

    def add_on_change(self, key: str, listener: Callable[[], None]) -> None:
        PluginSettings.load().add_on_change(key, listener)

    def clear_on_change(self, key: str) -> None:
        PluginSettings.load().clear_on_change(key)


class FormatterSettings(SettingsInterface):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def get(self, key: str, default: Any = None) -> Any:
        settings = PluginSettings.load()
        value = settings.get("formatters", {}).get(self._name, {}).get(key)
        return value if value is not None else settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        settings = PluginSettings.load()
        formatters = settings.setdefault("formatters", {})
        formatter = formatters.setdefault(self._name, {})
        formatter[key] = value
        settings["formatters"] = formatters
        PluginSettings.save()


class ProjectFormatSettings(SettingsInterface):
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
            ProjectFormatterSettings(name, self._window)
            for name in self.get("formatters", {})
        ]

    def formatter(self, name: str) -> Optional[ProjectFormatterSettings]:
        return (
            ProjectFormatterSettings(name, self._window)
            if name in self.get("formatters", {})
            else None
        )


class ProjectFormatterSettings(SettingsInterface):
    def __init__(self, name: str, window: Window) -> None:
        self._name = name
        self._window = window

    @property
    def name(self) -> str:
        return self._name

    def get(self, key: str, default: Any = None) -> Any:
        if not (project := self._window.project_data()):
            return default

        settings = project.get("settings", {}).get("Format", {})
        value = settings.get("formatters", {}).get(self._name, {}).get(key)
        return value if value is not None else project.get(key, default)

    def set(self, key: str, value: Any) -> None:
        project = self._window.project_data() or {}
        formatter_settings = (
            project.setdefault("settings", {})
            .setdefault("Format", {})
            .setdefault("formatters", {})
            .setdefault(self._name, {})
        )
        formatter_settings[key] = value
        self._window.set_project_data(project)
