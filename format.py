import sublime_plugin
import subprocess
import os

from .src.registry import formatter_for
from .src.settings import settings, save_settings


def process_startup_info():
    if not os.name == 'nt':
        return None
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    return startupinfo


def format(view, file=None, input=None):
    formatter = formatter_for(view)
    if not formatter:
        return None, 'No formatter for source file'

    command = formatter.command()
    args = formatter.file_args(file) if file else formatter.selection_args()
    return subprocess.Popen(
        command + args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=process_startup_info(),
        universal_newlines=True).communicate(input=input)


def print_error(error):
    print('Format:', error)


class FormatSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                continue

            selection = self.view.substr(region)
            output, error = format(self.view, input=selection)
            if not error:
                self.view.replace(edit, region, output)
            else:
                print_error(error)


class FormatFileCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return formatter_for(self.view) is not None

    def run(self, edit):
        output, error = format(self.view, file=self.view.file_name())
        if error:
            print_error(error)


class FormatListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        formatter = formatter_for(view)
        if formatter is not None and formatter.format_on_save:
            view.run_command('format_file')


class ToggleFormatOnSaveCommand(sublime_plugin.ApplicationCommand):
    def run(self, source=None):
        format_on_save = settings().get('format_on_save')
        settings().set('format_on_save', not format_on_save)
        save_settings()


class EnableFormatOnSaveCommand(ToggleFormatOnSaveCommand):
    def is_visible(self):
        return not settings().get('format_on_save')


class DisableFormatOnSaveCommand(ToggleFormatOnSaveCommand):
    def is_visible(self):
        return settings().get('format_on_save')
