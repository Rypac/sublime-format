import sublime_plugin

from .src.registry import FormatRegistry


def source_file(view):
    scope = view.scope_name(0) or ''
    return next(iter(scope.split(' ')))


def print_error(error):
    print('Format:', error)


registry = FormatRegistry()


class FormatSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        formatter = registry.for_source(source_file(self.view))
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
    def is_enabled(self):
        return registry.for_source(source_file(self.view)) is not None

    def run(self, edit):
        formatter = registry.for_source(source_file(self.view))
        if formatter is None:
            print_error('No formatter for source file')
            return

        output, error = formatter.format(file=self.view.file_name())
        if error:
            print_error(error)


class FormatListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        formatter = registry.for_source(source_file(view))
        if formatter and formatter.format_on_save:
            view.run_command('format_file')


class ToggleFormatOnSaveCommand(sublime_plugin.ApplicationCommand):
    def is_checked(self, name=None):
        if name is None:
            formatters = registry.all
            enabled = [x for x in formatters if x.format_on_save]
            return len(enabled) == len(formatters)
        else:
            formatter = registry.for_name(name)
            return formatter.format_on_save if formatter else False

    def run(self, name=None, value=None):
        if name is None:
            self.toggle_all()
        else:
            self.toggle(name, value)

    def toggle(self, name, value):
        formatter = registry.for_name(name)
        if formatter is not None:
            current = formatter.format_on_save
            formatter.format_on_save = not current if value is None else value

    def toggle_all(self):
        formatters = registry.all
        enabled = [x for x in formatters if x.format_on_save]
        enable = len(enabled) < len(formatters)
        for formatter in formatters:
            formatter.format_on_save = enable


class EnableFormatOnSaveCommand(ToggleFormatOnSaveCommand):
    def is_visible(self):
        formatter = registry.for_source(source_file(self.view))
        return not formatter.format_on_save if formatter else False

    def run(self, name, value):
        super(EnableFormatOnSaveCommand, self).run(name, value=True)


class DisableFormatOnSaveCommand(ToggleFormatOnSaveCommand):
    def is_visible(self):
        formatter = registry.for_source(source_file(self.view))
        return formatter.format_on_save if formatter else False

    def run(self, name, value):
        super(DisableFormatOnSaveCommand, self).run(name, value=False)
