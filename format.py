import sublime
import sublime_plugin

from .src import FormatterRegistry
from .src import Settings


def queue_command(callback, timeout=100):
    sublime.set_timeout(callback, timeout)


def log_error(error):
    print('Format:', error)


registry = FormatterRegistry()


def plugin_loaded():
    Settings.on_change(registry.populate)
    registry.populate()


def plugin_unloaded():
    Settings.stop_listening_for_changes()


def format_region(formatter, view, region, edit):
    selection = view.substr(region)
    output, error = formatter.format(selection)
    if not error:
        view.replace(edit, region, output)
    else:
        log_error(error)


class FormatSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        formatter = registry.by_view(self.view)
        if formatter:
            for region in self.view.sel():
                if not region.empty():
                    format_region(formatter, self.view, region, edit)
        else:
            log_error('No formatter for source file')


class FormatFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        formatter = registry.by_view(self.view)
        if formatter:
            region = sublime.Region(0, self.view.size())
            format_region(formatter, self.view, region, edit)
        else:
            log_error('No formatter for source file')


class FormatListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        formatter = registry.by_view(view)
        if formatter and formatter.format_on_save:
            view.run_command('format_file')


class ToggleFormatOnSaveCommand(sublime_plugin.ApplicationCommand):
    def is_checked(self, name=None):
        if name:
            formatter = registry.by_name(name)
            return formatter and formatter.format_on_save
        return all(f.format_on_save for f in registry.all)

    def run(self, name=None):
        if name:
            formatter = registry.by_name(name)
            if formatter:
                formatter.format_on_save = not formatter.format_on_save
        else:
            enable = any(not f.format_on_save for f in registry.all)
            for formatter in registry.all:
                formatter.format_on_save = enable


class ManageFormatOnSaveCommand(sublime_plugin.WindowCommand):
    def run(self, which=None):
        enabled = which == 'enabled'
        items = [[x.name]
                 for x in registry.by(lambda f: f.format_on_save == enabled)]

        def callback(selection):
            if selection >= 0 and selection < len(items):
                self.window.run_command('toggle_format_on_save',
                                        {'name': items[selection][0]})

        queue_command(lambda: self.window.show_quick_panel(items, callback))
