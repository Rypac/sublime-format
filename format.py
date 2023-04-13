from __future__ import annotations

from sublime import active_window, set_timeout_async, status_message
from sublime import Edit, View, Window
from sublime_plugin import ApplicationCommand, EventListener, TextCommand
from typing import cast

from .plugin import (
    FormatError,
    FormatterRegistry,
    display_error,
    clear_error,
    view_region,
    view_scope,
)


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
    def on_init(self, views: list[View]) -> None:
        def register_views():
            for view in views:
                registry.register(view)

        set_timeout_async(register_views)

    def on_new_async(self, view: View) -> None:
        registry.register(view)

    def on_close(self, view: View) -> None:
        registry.unregister(view)

    def on_load_project_async(self, window: Window) -> None:
        registry.update_window(window)

    def on_post_save_project_async(self, window: Window) -> None:
        registry.update_window(window)

    def on_pre_save(self, view: View) -> None:
        formatter = registry.lookup(view, view_scope(view))
        if formatter and formatter.settings.format_on_save:
            view.run_command("format_file")


class FormatFileCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        clear_error(self.view.window())

        if (region := view_region(self.view)).empty():
            return

        scope = view_scope(self.view)

        if formatter := registry.lookup(self.view, scope):
            try:
                formatter.format(self.view, edit, region)
            except FormatError as error:
                display_error(error, self.view.window())
        else:
            status_message(f"No formatter for file with scope: {scope}")

    def is_enabled(self) -> bool:
        return not view_region(self.view).empty()


class FormatSelectionCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        clear_error(self.view.window())

        for region in self.view.sel():
            if region.empty():
                continue

            scope = self.view.scope_name(region.begin())

            if formatter := registry.lookup(self.view, scope):
                try:
                    formatter.format(self.view, edit, region)
                except FormatError as error:
                    display_error(error, self.view.window())
                    break
            else:
                status_message(f"No formatter for selection with scope: {scope}")

    def is_enabled(self) -> bool:
        return any(not region.empty() for region in self.view.sel())


class FormatToggleEnabledCommand(ApplicationCommand):
    def run(self, name: str | None = None) -> None:
        settings = registry.settings.formatter(name) if name else registry.settings
        settings.set_enabled(not settings.enabled)

    def is_checked(self, name: str | None = None) -> bool:
        settings = registry.settings.formatter(name) if name else registry.settings
        return settings.enabled


class FormatManageEnabledCommand(ApplicationCommand):
    def run(self, enable: bool) -> None:
        items = [
            name
            for name, settings in registry.settings.formatters().items()
            if settings.enabled != enable
        ]

        def toggle_enabled(selection: int) -> None:
            if selection >= 0 and selection < len(items):
                formatter = items[selection]
                registry.settings.formatter(formatter).set_enabled(enable)

        if items:
            active_window().show_quick_panel(items, toggle_enabled)
        else:
            action = "enabled" if enable else "disabled"
            status_message(f"All formatters {action}.")


class FormatToggleFormatOnSaveCommand(ApplicationCommand):
    def run(self, name: str | None = None) -> None:
        settings = registry.settings.formatter(name) if name else registry.settings
        settings.set_format_on_save(not settings.format_on_save)

    def is_checked(self, name: str | None = None) -> bool:
        settings = registry.settings.formatter(name) if name else registry.settings
        return settings.format_on_save


class FormatManageFormatOnSaveCommand(ApplicationCommand):
    def run(self, enable: bool) -> None:
        items = [
            name
            for name, settings in registry.settings.formatters().items()
            if settings.format_on_save != enable
        ]

        def toggle_format_on_save(selection: int) -> None:
            if selection >= 0 and selection < len(items):
                formatter = items[selection]
                registry.settings.formatter(formatter).set_format_on_save(enable)

        if items:
            active_window().show_quick_panel(items, toggle_format_on_save)
        else:
            action = "enabled" if enable else "disabled"
            status_message(f"All formatters have format on save {action}.")
