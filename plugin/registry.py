from __future__ import annotations

from sublime import View, Window

from .configuration import Configuration
from .formatter import Formatter
from .settings import FormatSettings
from .view import view_scope


class FormatterRegistry:
    def __init__(self) -> None:
        self._settings: FormatSettings = None
        self._window_registries: Dict[int, WindowFormatterRegistry] = {}

    def startup(self) -> None:
        self._settings = FormatSettings()
        self._settings.add_on_change("reload_settings", self.update)
        self.update()

    def teardown(self) -> None:
        if settings := self._settings:
            settings.clear_on_change("reload_settings")
            self._settings = None
        self._window_registries.clear()

    def settings(self) -> FormatSettings:
        return self._settings

    def formatter_settings(self, name: str) -> FormatterSettings:
        return self._settings.formatter(name=formatter)

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

    def lookup(self, view: View, scope: str) -> Optional[Formatter]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if (window_registry := self._window_registries.get(window.id())) is None:
            return None

        return window_registry.by_scope(scope)

    def by_name(self, view: View, name: str) -> Optional[Formatter]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if (window_registry := self._window_registries.get(window.id())) is None:
            return None

        return window_registry.by_name(name)


class WindowFormatterRegistry:
    def __init__(self, window: Window, settings: FormatSettings) -> None:
        self._window: Window = window
        self._settings: FormatSettings = settings
        self._formatters: Dict[str, Formatter] = {}
        self.update()

    def update(self) -> None:
        formatter_configurations = self.project_configurations()

        self._formatters.clear()
        for name, config in formatter_configurations.items():
            self._formatters[name] = Formatter(name, config)

    def by_name(self, name: str) -> Optional[Formatter]:
        return self._formatters[name]

    def by_scope(self, scope: str) -> Optional[Formatter]:
        if not (formatters := self._formatters):
            return None

        formatter = max(formatters.values(), key=lambda f: f.score(scope))

        return formatter if formatter.score(scope) > 0 else None

    def project_configurations(self) -> Dict[str, Configuration]:
        settings = self._settings.to_dict()
        project_settings = (
            (self._window.project_data() or {}).get("settings", {}).get("Format", {})
        )
        config = Configuration.create(settings, project_settings)

        formatters = settings.get("formatters", {})
        project_formatters = project_settings.get("formatters", {})

        formatters_config = {}

        for name, formatter_settings in formatters.items():
            formatters_config[name] = (
                Configuration.create(config, project_overrides)
                if (project_overrides := project_formatters.pop(name, None))
                else Configuration.create(config, formatter_settings)
            )

        for name, formatter_settings in project_formatters.items():
            formatters_config[name] = Configuration.create(config, formatter_settings)

        return formatters_config
