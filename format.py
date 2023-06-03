from __future__ import annotations

from sublime import Edit, View, Window, active_window, status_message
from sublime_plugin import ApplicationCommand, EventListener, TextCommand, WindowCommand
from typing import cast

from .plugin.error import FormatError, clear_error, display_error
from .plugin.registry import FormatterRegistry
from .plugin.view import view_region, view_scope


registry: FormatterRegistry = cast(FormatterRegistry, None)


def plugin_loaded():
    global registry
    registry = FormatterRegistry()
    registry.startup()


def plugin_unloaded():
    global registry
    registry.teardown()
    registry = cast(FormatterRegistry, None)


class FormatListener(EventListener):
    def on_close(self, view: View) -> None:
        registry.unregister(view)

    def on_pre_move(self, view: View) -> None:
        registry.unregister(view)

    def on_load_project(self, window: Window) -> None:
        registry.update(window)

    def on_post_save_project(self, window: Window) -> None:
        registry.update(window)

    def on_pre_save(self, view: View) -> None:
        if (
            (formatter := registry.lookup(view, view_scope(view)))
            and formatter.settings.enabled
            and formatter.settings.format_on_save
        ):
            view.run_command("format_file")


class FormatFileCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        clear_error(self.view.window())

        if (region := view_region(self.view)).empty():
            return

        scope = view_scope(self.view)

        if not (formatter := registry.lookup(self.view, scope)):
            status_message(f"No formatter for file with scope: {scope}")
            return

        if formatter.settings.enabled:
            try:
                formatter.format(self.view, edit, region)
            except FormatError as error:
                display_error(error, self.view.window())
        else:
            status_message(f"Formatter disabled: {formatter.name}")

    def is_enabled(self) -> bool:
        return not view_region(self.view).empty()


class FormatSelectionCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        clear_error(self.view.window())

        for region in self.view.sel():
            if region.empty():
                continue

            scope = self.view.scope_name(region.begin())

            if not (formatter := registry.lookup(self.view, scope)):
                status_message(f"No formatter for selection with scope: {scope}")
                continue

            if formatter.settings.enabled:
                try:
                    formatter.format(self.view, edit, region)
                except FormatError as error:
                    display_error(error, self.view.window())
            else:
                status_message(f"Formatter disabled: {formatter.name}")

    def is_enabled(self) -> bool:
        return any(not region.empty() for region in self.view.sel())


class FormatToggleEnabledCommand(ApplicationCommand):
    def run(self, name: str | None = None) -> None:
        settings = registry.settings.formatter(name) if name else registry.settings
        settings.enabled = not settings.enabled

    def is_checked(self, name: str | None = None) -> bool:
        settings = registry.settings.formatter(name) if name else registry.settings
        return settings.enabled


class FormatToggleFormatOnSaveCommand(ApplicationCommand):
    def run(self, name: str | None = None) -> None:
        settings = registry.settings.formatter(name) if name else registry.settings
        settings.format_on_save = not settings.format_on_save

    def is_checked(self, name: str | None = None) -> bool:
        settings = registry.settings.formatter(name) if name else registry.settings
        return settings.format_on_save


class FormatManageEnabledCommand(WindowCommand):
    def run(self, enable: bool, project: bool = False) -> None:
        settings = (
            registry.project_settings(self.window) if project else registry.settings
        )

        items = [
            name
            for name, formatter_settings in settings.formatters().items()
            if formatter_settings.enabled != enable
        ]

        def toggle_enabled(selection: int) -> None:
            if selection >= 0 and selection < len(items):
                formatter = items[selection]
                settings.formatter(formatter).enabled = enable

        if items:
            active_window().show_quick_panel(items, toggle_enabled)
        else:
            action = "enabled" if enable else "disabled"
            status_message(f"All formatters {action}.")


class FormatManageFormatOnSaveCommand(WindowCommand):
    def run(self, enable: bool, project: bool = False) -> None:
        settings = (
            registry.project_settings(self.window) if project else registry.settings
        )

        items = [
            name
            for name, formatter_settings in settings.formatters().items()
            if formatter_settings.format_on_save != enable
        ]

        def toggle_format_on_save(selection: int) -> None:
            if selection >= 0 and selection < len(items):
                formatter = items[selection]
                settings.formatter(formatter).format_on_save = enable

        if items:
            active_window().show_quick_panel(items, toggle_format_on_save)
        else:
            action = "enabled" if enable else "disabled"
            status_message(f"All formatters have format on save {action}.")
