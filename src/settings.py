import sublime


class Settings():
    @staticmethod
    def load():
        return sublime.load_settings('Format.sublime-settings')

    @staticmethod
    def save():
        sublime.save_settings('Format.sublime-settings')

    @staticmethod
    def on_change(callback):
        Settings.load().add_on_change('Format.sublime-settings', callback)

    @staticmethod
    def formatters():
        return Settings.load().get('formatters', default={})

    @staticmethod
    def paths():
        return Settings.load().get('paths', default=[])

    @staticmethod
    def update_formatter(name, value):
        settings = Settings.load()
        formatters = Settings.formatters()
        formatters[name] = value
        settings.set('formatters', formatters)
        Settings.save()


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
