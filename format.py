import sublime
import sublime_plugin

from .src.registry import FormatterRegistry
from .src.settings import Settings


def queue_command(callback, timeout=100):
    sublime.set_timeout(callback, timeout)


def perform_in_background(callback, timeout=0):
    sublime.set_timeout_async(callback, timeout)


def print_error(error):
    print('Format:', error)


registry = FormatterRegistry()


def plugin_loaded():
    def load_formatters():
        registry.populate()

    def prepare_plugin():
        Settings.upgrade()
        Settings.on_change(load_formatters)
        load_formatters()

    perform_in_background(prepare_plugin)


def plugin_unloaded():
    Settings.stop_listening_for_changes()


class FormatSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        formatter = registry.by_view(self.view)
        if formatter is None:
            print_error('No formatter for source file')
            return

        for region in self.view.sel():
            if region.empty():
                continue

            selection = self.view.substr(region)
            output, error = formatter.format(input=selection)
            if not error:
                self.view.replace(edit, region, output)
            else:
                print_error(error)


class FormatFileCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self.formatter = registry.by_view(view)

    def is_enabled(self):
        return self.formatter is not None

    def run(self, edit):
        output, error = self.formatter.format(file=self.view.file_name())
        if not error:
            queue_command(lambda: self.view.run_command('revert'))
        else:
            print_error(error)


class FormatListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        formatter = registry.by_view(view)
        if formatter and formatter.format_on_save:
            view.run_command('format_file')


class ToggleFormatOnSaveCommand(sublime_plugin.ApplicationCommand):
    def is_checked(self, name=None):
        if name:
            formatter = registry.by_name(name)
            return formatter and formatter.format_on_save
        return len(registry.enabled) == len(registry.all)

    def run(self, name=None, value=None):
        if name:
            self.toggle(name, value)
        else:
            self.toggle_all()

    def toggle(self, name, value):
        formatter = registry.by_name(name)
        if formatter:
            current = formatter.format_on_save
            formatter.format_on_save = not current if value is None else value

    def toggle_all(self):
        enable = len(registry.enabled) < len(registry.all)
        for formatter in registry.all:
            formatter.format_on_save = enable


class ManageFormatOnSaveCommand(sublime_plugin.WindowCommand):
    def run(self, which=None):
        enabled = which == 'enabled'
        items = [[x.name] for x in registry.all if x.format_on_save == enabled]

        def callback(selection):
            if selection >= 0 and selection < len(items):
                args = {'name': items[selection][0]}
                self.window.run_command('toggle_format_on_save', args)

        queue_command(lambda: self.window.show_quick_panel(items, callback))
