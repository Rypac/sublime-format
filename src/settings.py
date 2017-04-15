import sublime


class Settings():
    FORMAT_SETTINGS = 'Format.sublime-settings'

    @staticmethod
    def load():
        return sublime.load_settings(Settings.FORMAT_SETTINGS)

    @staticmethod
    def save():
        sublime.save_settings(Settings.FORMAT_SETTINGS)

    @staticmethod
    def on_change(callback):
        Settings.load().add_on_change(Settings.FORMAT_SETTINGS, callback)

    @staticmethod
    def stop_listening_for_changes():
        Settings.load().clear_on_change(Settings.FORMAT_SETTINGS)

    @staticmethod
    def formatters():
        return Settings.load().get('formatters', default={})

    @staticmethod
    def paths():
        return Settings.load().get('paths', default=[])

    @staticmethod
    def update_formatter(name, value):
        formatters = Settings.formatters()
        formatters[name] = value
        Settings.update_formatters(formatters)

    @staticmethod
    def update_formatters(value):
        Settings.load().set('formatters', value)
        Settings.save()

    @staticmethod
    def upgrade():
        try:
            path = 'Packages/Format/' + Settings.FORMAT_SETTINGS
            resources = sublime.load_resource(path)
            settings = sublime.decode_value(resources)
            formatters = settings.get('formatters', {})
            formatters.update(Settings.formatters())
            Settings.update_formatters(formatters)
        except Exception:
            return


class FormatterSettings():
    def __init__(self, formatter):
        self.__formatter = formatter
        self.__settings = Settings.formatters().get(formatter, {})

    def get(self, value, default=None):
        return self.__settings.get(value, default)

    def set(self, key, value):
        self.__settings[key] = value
        Settings.update_formatter(self.__formatter, self.__settings)

    @property
    def format_on_save(self):
        return self.get('format_on_save', default=False)

    @format_on_save.setter
    def format_on_save(self, value):
        return self.set('format_on_save', value)

    @property
    def sources(self):
        return self.get('sources', default=[])

    @property
    def args(self):
        return self.get('args', default=[])
