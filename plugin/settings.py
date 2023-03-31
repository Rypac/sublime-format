from __future__ import annotations

from sublime import load_settings, save_settings, Settings, Window
from typing import Any, Dict, List, Optional


class PluginSettings:
    @staticmethod
    def load() -> Settings:
        return load_settings("Format.sublime-settings")

    @staticmethod
    def load_project(window: Window) -> Dict[str, Any]:
        return (window.project_data() or {}).get("settings", {}).get("Format", {})

    @staticmethod
    def save() -> None:
        save_settings("Format.sublime-settings")


class SettingsInterface:
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves a value from settings for the given key, with an optional default."""
        pass

    def set(self, key: str, value: Any) -> None:
        """Stores a value in settings for the given key."""
        pass

    def reload(self) -> None:
        """Reloads settings if invalidated."""
        pass

    @property
    def selector(self) -> str:
        return self.get("selector")

    @property
    def cmd(self) -> List[str]:
        return self.get("cmd")

    @property
    def enabled(self) -> bool:
        return self.get("enabled", True)

    def set_enabled(self, enabled: bool) -> None:
        return self.set("enabled", enabled)

    @property
    def format_on_save(self) -> bool:
        return self.get("format_on_save", False)

    def set_format_on_save(self, enabled: bool) -> None:
        return self.set("format_on_save", enabled)

    @property
    def error_style(self) -> str:
        return self.get("error_style", "panel")

    @property
    def timeout(self) -> int:
        return self.get("timeout", 60)


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


class WindowFormatterSettings(SettingsInterface):
    def __init__(self, name: str, window: Window):
        self._name = name
        self._window = window
        self._settings = {}  # type: Dict[str, Any]
        self.reload()

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        raise Exception("WindowFormatterSettings are read-only.")

    def reload(self) -> None:
        settings = PluginSettings.load().to_dict()
        formatter = settings.get("formatters", {}).get(self._name, {})

        project = PluginSettings.load_project(self._window)
        project_formatter = project.get("formatters", {}).get(self._name, {})

        self._settings.clear()
        for source in (settings, project, formatter, project_formatter):
            for key, value in source.items():
                if key != "formatters":
                    self._settings[key] = value
