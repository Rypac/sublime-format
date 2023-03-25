from __future__ import annotations

from sublime import Edit, View, Window
from sublime_plugin import ApplicationCommand, EventListener, TextCommand, ViewEventListener, WindowCommand
from typing import Optional

from .plugin import FormatterRegistry


def queue_command(callback, timeout=100):
    sublime.set_timeout(callback, timeout)


def log_error(output, error):
    print('Format:', output, error)


registry = None  # type: Optional[FormatterRegistry]


def plugin_loaded():
    global registry
    registry = FormatterRegistry()
    registry.setup()


def plugin_unloaded():
    global registry
    registry.teardown()
    registry = None


def format_region(formatter, view, region, edit):
    selection = view.substr(region)
    ok, output, error = formatter.format(selection, settings=view.settings())
    if ok:
        view.replace(edit, region, output)
    else:
        log_error(output, error)


class ProjectSettingsListener(EventListener):
    def on_init(self, views: list[View]) -> None:
        window_ids = set()
        for view in views:
            if (window := view.window()) is not None and window.id() not in window_ids:
                window_ids.add(window.id())
                registry.register(window)

    def on_load_project_async(self, window: Window) -> None:
        registry.update(window)

    def on_post_save_project_async(self, window: Window) -> None:
        registry.update(window)

    def on_pre_close_window(self, window: Window) -> None:
        registry.unregister(window)


class FormatListener(ViewEventListener):
    def on_pre_save(self, view: View) -> None:
        formatter = registry.by_view(view)
        if formatter and formatter.enabled and formatter.format_on_save:
            view.run_command('format_file')


class FormatSelectionCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        formatter = registry.by_view(self.view)
        if formatter:
            for region in self.view.sel():
                if not region.empty():
                    format_region(formatter, self.view, region, edit)
        else:
            log_error('No formatter for source file')

    def is_enabled(self) -> bool:
        return any(not region.empty() for region in self.view.sel())


class FormatFileCommand(TextCommand):
    def run(self, edit: Edit) -> None:
        formatter = registry.by_view(self.view)
        if formatter:
            region = sublime.Region(0, self.view.size())
            format_region(formatter, self.view, region, edit)
        else:
            log_error('No formatter for source file')

    def is_enabled(self) -> bool:
        return not Region(0, self.view.size()).empty()


class ToggleFormatOnSaveCommand(ApplicationCommand):
    def run(self, name: Optional[str] = None) -> None:
        if name:
            formatter = registry.by_name(name)
            if formatter:
                formatter.format_on_save = not formatter.format_on_save
        else:
            enable = any(not f.format_on_save for f in registry.all)
            for formatter in registry.all:
                formatter.format_on_save = enable

    def is_checked(self, name: Optional[str] = None) -> bool:
        if name:
            formatter = registry.by_name(name)
            return formatter and formatter.format_on_save
        return all(f.format_on_save for f in registry.all)


class ManageFormatOnSaveCommand(WindowCommand):
    def run(self, which=None) -> None:
        enabled = which == 'enabled'
        items = [[x.name]
                 for x in registry.by(lambda f: f.format_on_save == enabled)]

        def callback(selection):
            if selection >= 0 and selection < len(items):
                self.window.run_command('toggle_format_on_save',
                                        {'name': items[selection][0]})

        queue_command(lambda: self.window.show_quick_panel(items, callback))
