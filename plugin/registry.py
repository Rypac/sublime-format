from __future__ import annotations

from sublime import View

from .formatter import Formatter


class FormatterRegistry:
    def __init__(self) -> None:
        self._configurations = {}  # type: Dict[str, Configuration]
        self._windows = {}  # type: Dict[int, Window]
        self._window_configurations = {}  # type: Dict[int, Dict[str, Configuration]]
        self._formatters = {}  # type: Dict[int, Dict[str, Formatter]]

    def startup(self) -> None:
        settings = load_settings("RyTest.sublime-settings")
        settings.add_on_change("reload_settings", self.update)
        for window in sublime.windows():
            pass

    def teardown(self) -> None:
        settings = load_settings("RyTest.sublime-settings")
        settings.clear_on_change("reload_settings")

        self._configurations = {}
        self._window_configurations = {}

    def register(self, window: Window) -> None:
        pass

    def unregister(self, window: Window) -> None:
        window_id = window.id()

        if window_id in self._windows:
            del self._windows[window_id]

        if window_id in self._window_configurations:
            del self._window_configurations[window_id]

    def update(self) -> None:
        settings = load_settings("RyTest.sublime-settings")
        formatters = settings.get("formatters", {})
        self._configurations.clear()
        self._configurations.update(
            {
                name: create_configuration(settings, name)
                for name, d in formatters.get().items()
            }
        )

        project_settings = (
            (self._window.project_data() or {}).get("settings", {}).get(PLUGIN_NAME, {})
        )
        self._formatter_configurations.clear()

        for name, config in self._global_configs.items():
            overrides = project_settings.pop(name, {})
            self._formatter_configurations[name] = GlobalConfiguration.from_config(
                config, overrides
            )

        for name, config in project_settings.items():
            self._formatter_configurations[name] = GlobalConfiguration.from_dict(name, config)

    def lookup(self, view: View, scope: Optional[str] = None) -> Optional[Configuration]:
        if (window := view.window()) is None or not window.is_valid():
            return None

        if (formatters := self._window_configurations.get(window.id())) is None:
            return None

        pass

    def enable(self, name: Optional[str] = None) -> None:
        self._set_enabled(name, True)

    def disable(self, name: Optional[str] = None) -> None:
        self._set_enabled(name, False)

    def _set_enabled(self, name: Optional[str], is_enabled: bool) -> None:
        with edit_settings("RyTest.sublime-settings") as settings:
            if name:
                formatters = settings.get("formatters")
                config = formatters.setdefault(name, {})
                config["enabled"] = is_enabled
                settings["formatters"] = formatters
            else:
                settings["enabled"] = is_enabled

    def enable_format_on_save(self, name: Optional[str] = None) -> None:
        self._set_format_on_save_enabled(name, True)

    def disable_format_on_save(self, name: Optional[str] = None) -> None:
        self._set_format_on_save_enabled(name, False)

    def _set_format_on_save_enabled(self, name: Optional[str], is_enabled: bool) -> None:
        with edit_settings("RyTest.sublime-settings") as settings:
            if name:
                formatters = settings.get("formatters")
                config = formatters.setdefault(name, {})
                config["format_on_save"] = is_enabled
                settings["formatters"] = formatters
            else:
                settings["format_on_save"] = is_enabled
