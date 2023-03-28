from __future__ import annotations

from sublime import active_window
from sublime import Edit, Region, View, Window
from sublime_plugin import ApplicationCommand, EventListener, TextCommand
from typing import Optional

from .plugin import FormatterRegistry


registry: Optional[FormatterRegistry] = None


def plugin_loaded():
    global registry
    registry = FormatterRegistry()
    registry.startup()


def plugin_unloaded():
    global registry
    registry.teardown()
    registry = None


class FormatListener(EventListener):
    def on_init(self, views: list[View]) -> None:
        window_ids = set()
        for view in views:
            if (window := view.window()) and window.id() not in window_ids:
                window_ids.add(window.id())
                registry.register(window)

    def on_exit(self) -> None:
        registry.teardown()

    def on_new_window_async(self, window: Window) -> None:
        registry.register(window)

    def on_pre_close_window(self, window: Window) -> None:
        registry.unregister(window)

    def on_load_project_async(self, window: Window) -> None:
        registry.update_window(window)

    def on_post_save_project_async(self, window: Window) -> None:
        registry.update_window(window)

    def on_pre_save(self, view: View) -> None:
        formatter = registry.lookup(view)
        if formatter and formatter.enabled and formatter.format_on_save:
            view.run_command("format_file")


class FormatFileCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        region = Region(0, self.view.size())
        if region.empty():
            return

        if formatter := registry.lookup(self.view):
            if formatter.enabled:
                try:
                    formatter.format(self.view, edit, region)
                except Exception as err:
                    print("[Format]", err)
        else:
            print("[Format]", "No formatter for file")

    def is_enabled(self) -> bool:
        return not Region(0, self.view.size()).empty()


class FormatSelectionCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        for region in self.view.sel():
            if region.empty():
                continue

            scope = self.view.scope_name(region.begin())
            if formatter := registry.lookup(self.view, scope):
                if formatter.enabled:
                    try:
                        formatter.format(self.view, edit, region)
                    except Exception as err:
                        print("[Format]", err)
            else:
                print("[Format]", "No formatter for selection")

    def is_enabled(self) -> bool:
        return any(not region.empty() for region in self.view.sel())


class FormatToggleEnabledCommand(ApplicationCommand):
    def run(self, name: Optional[str] = None) -> None:
        settings = registry.settings(name)
        enabled = settings.enabled()
        settings.set_enabled(not enabled)

    def is_checked(self, name: Optional[str] = None) -> bool:
        return registry.settings(name).enabled()


class FormatManageEnabledCommand(ApplicationCommand):
    def run(self, enable: bool) -> None:
        items = [
            formatter.name
            for formatter in registry.settings().formatters()
            if formatter.enabled() != enable
        ]

        def toggle_enabled(selection: int) -> None:
            if selection > 0 and selection < len(items):
                formatter = items[selection]
                registry.settings(formatter).set_enabled(enable)

        if items:
            active_window().show_quick_panel(items, toggle_enabled)


class FormatToggleFormatOnSaveCommand(ApplicationCommand):
    def run(self, name: Optional[str] = None) -> None:
        settings = registry.settings(name)
        enabled = settings.format_on_save()
        settings.set_format_on_save(not enabled)

    def is_checked(self, name: Optional[str] = None) -> bool:
        return registry.settings(name).format_on_save()


class FormatManageFormatOnSaveCommand(ApplicationCommand):
    def run(self, enable: bool) -> None:
        items = [
            formatter.name
            for formatter in registry.settings().formatters()
            if formatter.format_on_save() != enable
        ]

        def toggle_format_on_save(selection: int) -> None:
            if selection > 0 and selection < len(items):
                formatter = items[selection]
                registry.settings(formatter).set_format_on_save(enable)

        if items:
            active_window().show_quick_panel(items, toggle_format_on_save)
