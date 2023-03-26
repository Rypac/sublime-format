from __future__ import annotations

from sublime import Settings, View

from .configuration import Configuration
from .formatter import Formatter
from .settings import edit_settings
from .view import view_scope


class FormatterRegistry:
    def __init__(self) -> None:
        self._settings = None  # type: Settings
        self._configurations = {}  # type: Dict[str, Configuration]
        self._windows = {}  # type: Dict[int, Window]
        self._formatters = {}  # type: Dict[int, Dict[str, Formatter]]

    def startup(self) -> None:
        self._settings = sublime.load_settings("Format.sublime-settings")
        self._settings.add_on_change("reload_settings", self.update)
        self.update()

    def teardown(self) -> None:
        self._settings.clear_on_change("reload_settings")
        self._settings = None

        self._configurations.clear()
        self._windows.clear()
        self._formatters.clear()

    def register(self, window: Window) -> None:
        if window.is_valid():
            self._windows[window.id()] = window
            self.update_window(window)

    def unregister(self, window: Window) -> None:
        window_id = window.id()

        if window_id in self._windows:
            del self._windows[window_id]

        if window_id in self._formatters:
            del self._formatters[window_id]

    def update(self) -> None:
        formatters = self._settings.get("formatters", {})
        self._configurations.clear()
        self._configurations.update(
            {
                name: Configuration.create(settings, formatter_settings)
                for name, formatter_settings in formatters.items()
            }
        )

        self._formatters.clear()
        for window in self._windows.values():
            self.update_window(window)

    def update_window(self, window: Window) -> None:
        window_id = window.id()

        self._formatters[window_id] = {}

        if project_settings := (window.project_data() or {}).get("settings", {}).get("Format"):
            project_config = Configuration.create(settings, project_settings)

            project_formatter_settings = project_settings.get("formatters", {})

            for name, config in self._configurations.items():
                formatter_settings = project_formatter_settings.pop(name, {})
                project_config = Configuration.create(project_config, formatter_settings)
                self._formatters[window_id][name] = Formatter(name, project_config)

            for name, formatter_settings in project_formatter_settings.items():
                project_config = Configuration.create(project_config, formatter_settings)
                self._formatters[window_id][name] = Formatter(name, project_config)
        else:
            for name, config in self._configurations.items():
                self._formatters[window_id][name] = Formatter(name, config)

    def lookup(self, view: View, scope: Optional[str] = None) -> Optional[Formatter]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if not (formatters := self._formatters.get(window.id())):
            return None

        formatter_scope = score or view_scope(view)

        formatter = max(formatters, key=lambda f: f.score(formatter_scope))

        return formatter if formatter.score(formatter_scope) > 0 else None

    def by_name(self, view: View, name: str) -> Optional[Formatter]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        return formatters.get(name) if (formatters := self._formatters.get(window.id())) else None

    def is_enabled(self, name: Optional[str] = None) -> bool:
        return self._settings.get("enabled", default=True)

    def enable(self, name: Optional[str] = None) -> None:
        self._set_enabled(name, True)

    def disable(self, name: Optional[str] = None) -> None:
        self._set_enabled(name, False)

    def _set_enabled(self, name: Optional[str], is_enabled: bool) -> None:
        with edit_settings("Format.sublime-settings") as settings:
            if name:
                formatters = settings.get("formatters")
                config = formatters.setdefault(name, {})
                config["enabled"] = is_enabled
                settings["formatters"] = formatters
            else:
                settings["enabled"] = is_enabled

    def is_format_on_save_enabled(self, name: Optional[str] = None) -> bool:
        return self._settings.get("format_on_save", default=False)

    def enable_format_on_save(self, name: Optional[str] = None) -> None:
        self._set_format_on_save_enabled(name, True)

    def disable_format_on_save(self, name: Optional[str] = None) -> None:
        self._set_format_on_save_enabled(name, False)

    def _set_format_on_save_enabled(self, name: Optional[str], is_enabled: bool) -> None:
        with edit_settings("Format.sublime-settings") as settings:
            if name:
                formatters = settings.get("formatters")
                config = formatters.setdefault(name, {})
                config["format_on_save"] = is_enabled
                settings["formatters"] = formatters
            else:
                settings["format_on_save"] = is_enabled

