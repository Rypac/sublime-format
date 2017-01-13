import sublime


class Settings():
    def __init__(self, formatter):
        self.__formatter = formatter

    def load(self):
        return sublime.load_settings('Format.sublime-settings')

    def save(self):
        sublime.save_settings('Format.sublime-settings')

    def get(self, value, default=None):
        return self.load().get(self.__formatter, {}).get(value, default)

    def set(self, key, value):
        settings = self.load()
        formatter_settings = settings.get(self.__formatter, {})
        formatter_settings[key] = value
        settings.set(self.__formatter, formatter_settings)
        self.save()


class Formatter(object):
    def __init__(self, name=None, source=None, binary=None):
        self.__name = name
        self.__source = 'source.' + (source if source else name.lower())
        self.__binary = binary

    def settings(self):
        return Settings(self.name.lower())

    @property
    def name(self):
        return self.__name

    @property
    def source(self):
        return self.__source

    @property
    def binary(self):
        return self.settings().get('binary', self.__binary)

    @property
    def format_on_save(self):
        return self.settings().get('format_on_save', False)

    @format_on_save.setter
    def format_on_save(self, value):
        self.settings().set('format_on_save', value)

    def command(self):
        return [self.binary]

    def selection_args(self):
        return []

    def file_args(self, file_name):
        return [file_name]
