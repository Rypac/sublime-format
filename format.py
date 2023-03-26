from __future__ import annotations

from sublime import Edit, View, Window
from sublime_plugin import (
    ApplicationCommand,
    EventListener,
    TextCommand,
    ViewEventListener,
)
from typing import Optional

from .plugin import FormatterRegistry


registry = None  # type: Optional[FormatterRegistry]


def plugin_loaded():
    global registry
    registry = FormatterRegistry()
    registry.setup()


def plugin_unloaded():
    global registry
    registry.teardown()
    registry = None


class RegistryListener(EventListener):
    def on_init(self, views: list[View]) -> None:
        window_ids = set()
        for view in views:
            if (window := view.window()) and window.id() not in window_ids:
                window_ids.add(window.id())
                registry.register(window)

    def on_load_project_async(self, window: Window) -> None:
        registry.update_window(window)

    def on_post_save_project_async(self, window: Window) -> None:
        registry.update_window(window)

    def on_pre_close_window(self, window: Window) -> None:
        registry.unregister(window)


class FormatListener(ViewEventListener):
    def on_pre_save(self, view: View) -> None:
        formatter = registry.lookup(view)
        if formatter and formatter.enabled and formatter.format_on_save:
            view.run_command("format_file")


class FormatFileCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        if formatter := registry.lookup(self.view):
            region = Region(0, self.view.size())

            if not region.empty() and formatter.enabled:
                formatter.format(self.view, edit, region)
        else:
            print("[Format]", "No formatter for file")

    def is_enabled(self) -> bool:
        return not Region(0, self.view.size()).empty()


class FormatSelectionCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        for region in self.view.sel():
            if region.empty():
                continue

            if formatter := registry.lookup(self.view):
                if formatter.enabled:
                    formatter.format(self.view, edit, region)
            else:
                print("[Format]", "No formatter for selection")

    def is_enabled(self) -> bool:
        return any(not region.empty() for region in self.view.sel())


class FormatEnableCommand(ApplicationCommand):
    def run(self, name: Optional[str] = None) -> None:
        registry.enable(name)

    def is_enabled(self, name: Optional[str] = None) -> bool:
        return not registry.is_enabled(name)


class FormatDisableCommand(ApplicationCommand):
    def run(self, name: Optional[str] = None) -> None:
        registry.disable(name)

    def is_enabled(self, name: Optional[str] = None) -> bool:
        return registry.is_enabled(name)


class FormatEnableFormatOnSaveCommand(ApplicationCommand):
    def run(self, name: Optional[str] = None) -> None:
        registry.enable_format_on_save(name)

    def is_enabled(self, name: Optional[str] = None) -> bool:
        return not registry.is_format_on_save_enabled(name)


class FormatDisableFormatOnSaveCommand(ApplicationCommand):
    def run(self, name: Optional[str] = None) -> None:
        registry.disable_format_on_save(name)

    def is_enabled(self, name: Optional[str] = None) -> bool:
        return registry.is_format_on_save_enabled(name)
