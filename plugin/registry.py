from __future__ import annotations

from sublime import View, Window

from .configuration import Configuration
from .formatter import Formatter
from .settings import FormatterSettings
from .view import view_scope


class FormatterRegistry:
    def __init__(self) -> None:
        self._settings: FormatterSettings = None
        self._window_registries: Dict[int, WindowFormatterRegistry] = {}

    def startup(self) -> None:
        self._settings = FormatterSettings()
        self._settings.add_on_change("reload_settings", self.update)
        self.update()

    def teardown(self) -> None:
        if settings := self._settings:
            settings.clear_on_change("reload_settings")
            self._settings = None
        self._window_registries.clear()

    def settings(self, formatter: Optional[str] = None) -> FormatterSettings:
        return self._settings.formatter(name=formatter) if formatter else self._settings

    def register(self, window: Window) -> None:
        if not window.is_valid() or window.id() in self._window_registries:
            return

        window_registry = WindowFormatterRegistry(window, self._settings)
        self._window_registries[window.id()] = window_registry

    def unregister(self, window: Window) -> None:
        if (window_id := window.id()) in self._window_registries:
            del self._window_registries[window_id]

    def update(self) -> None:
        for window_registry in self._window_registries.values():
            window_registry.update()

    def update_window(self, window: Window) -> None:
        if window_registry := self._window_registries.get(window.id()):
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


class WindowFormatterRegistry:
    def __init__(self, window: Window, settings: FormatterSettings) -> None:
        self._window: Window = window
        self._settings: FormatterSettings = settings
        self._formatters: Dict[str, Formatter] = {}
        self.update()

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
            or not (project_format_settings := project_settings.get("Format"))
        ):
            return settings

        merged_settings = {}

        for key, value in settings.items():
            if key == "formatters":
                if formatter_settings := project_format_settings.get(key):
                    merged_settings[key] = {**value, **formatter_settings}
                else:
                    merged_settings[key] = value
            else:
                merged_settings[key] = project_format_settings.get(key, value)

        return merged_settings
