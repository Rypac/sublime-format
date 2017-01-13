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
