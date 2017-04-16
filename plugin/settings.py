import sublime

PLUGIN_NAME = 'Format'
PLUGIN_SETTINGS = '{}.sublime-settings'.format(PLUGIN_NAME)


class Settings:
    @staticmethod
    def load():
        return sublime.load_settings(PLUGIN_SETTINGS)

    @staticmethod
    def save():
        sublime.save_settings(PLUGIN_SETTINGS)

    @staticmethod
    def on_change(callback):
        Settings.load().add_on_change(PLUGIN_NAME, callback)

    @staticmethod
    def stop_listening_for_changes():
        Settings.load().clear_on_change(PLUGIN_NAME)

    @staticmethod
    def formatter(name):
        return Settings.load().get('{}_formatter'.format(name), default={})

    @staticmethod
    def paths():
        return Settings.load().get('paths', default=[])

    @staticmethod
    def update_formatter(name, value):
        Settings.load().set('{}_formatter'.format(name), value)
        Settings.save()


class FormatterSettings:
    def __init__(self, name):
        self.__name = name
        self.__settings = Settings.formatter(name)

    def get(self, value, default=None):
        return self.__settings.get(value, default)

    def set(self, key, value):
        self.__settings[key] = value
        Settings.update_formatter(self.__name, self.__settings)

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
    def options(self):
        return self.get('options', default=[])
