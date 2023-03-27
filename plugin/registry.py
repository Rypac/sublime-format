from __future__ import annotations

from sublime import load_settings, Settings, View, Window

from .configuration import Configuration
from .formatter import Formatter
from .settings import edit_settings
from .view import view_scope


class FormatterRegistry:
    def __init__(self) -> None:
        self._settings = None  # type: Settings
        self._window_registries = {}  # type: Dict[int, WindowFormatterRegistry]

    def startup(self) -> None:
        self._settings = load_settings("Format.sublime-settings")
        self._settings.add_on_change("reload_settings", self.update)
        self.update()

    def teardown(self) -> None:
        if settings := self._settings:
            settings.clear_on_change("reload_settings")
            self._settings = None
        self._window_registries.clear()

    def register(self, window: Window) -> None:
        if not window.is_valid() or window.id() in self._window_registries:
            return

        window_registry = WindowFormatterRegistry(window, self._settings)
        window_registry.update()
        self._window_registries[window.id()] = window_registry

    def unregister(self, window: Window) -> None:
        if (window_id := window.id()) in self._window_registries:
            del self._window_registries[window_id]

    def update(self) -> None:
        for window_registry in self._window_registries.values():
            window_registry.update()

    def update_window(self, window: Window) -> None:
        if (window_registry := self._window_registries.get(window.id())):
            window_registry.update()

    def lookup(self, view: View, scope: Optional[str] = None) -> Optional[Formatter]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if (window_registry := self._window_registries.get(window.id())) is None:
            return None

        return window_registry.by_scope(scope or view_scope(view))

    def by_name(self, view: View, name: str) -> Optional[Formatter]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if (window_registry := self._window_registries.get(window.id())) is None:
            return None

        return window_registry.by_name(name)

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
                formatter = formatters.setdefault(name, {})
                formatter["enabled"] = is_enabled
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
                formatter = formatters.setdefault(name, {})
                formatter["format_on_save"] = is_enabled
                settings["formatters"] = formatters
            else:
                settings["format_on_save"] = is_enabled


class WindowFormatterRegistry:
    def __init__(self, window: Window, settings: Settings) -> None:
        self._window = window  # type: Window
        self._settings = settings  # type: Settings
        self._formatters = {}  # type: Dict[str, Formatter]

    def update(self) -> None:
        project_settings = self._merged_project_settings()
        project_formatters = project_settings.get("formatters", {})

        self._formatters.clear()
        for name, formatter_settings in project_formatters.items():
            config = Configuration.create(project_settings, formatter_settings)
            self._formatters[name] = Formatter(name, config)

    def by_name(self, name: str) -> Optional[Formatter]:
        return self._formatters[name]

    def by_scope(self, scope: str) -> Optional[Formatter]:
        if not (formatters := self._formatters):
            return None

        formatter = max(formatters.values(), key=lambda f: f.score(scope))

        return formatter if formatter.score(scope) > 0 else None

    def _merged_project_settings(self) -> Dict[str, Any]:
        settings = self._settings.to_dict()

        if (
            not (project_data := self._window.project_data())
            or not (project_settings := project_data.get("settings"))
            or not (format_settings := project_settings.get("Format"))
        ):
            return settings

        merged_settings = {}

        for key, value in settings.to_dict().items():
            if key == "formatters":
                if (formatter_settings := format_settings.get(key)):
                    merged_settings[key] = {**value, **formatter_settings}
                else:
                    merged_settings[key] = value
            else:
                merged_settings[key] = format_settings.get(key, value)

        return merged_settings
