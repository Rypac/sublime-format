import sublime


class Settings:
    def __init__(self):
        self.__settings_key = 'Format.sublime-settings'

    def add_observer(self, key, observer):
        self.__load().add_on_change(self.__observer_id(key), observer)

    def remove_observer(self, key):
        self.__load().clear_on_change(self.__observer_id(key))

    def formatter(self, name):
        return self.__load().get('{}_formatter'.format(name), default={})

    def paths(self):
        return self.__load().get('paths', default=[])

    def update_formatter(self, name, value):
        self.__load().set('{}_formatter'.format(name), value)
        self.__save()

    def __load(self):
        return sublime.load_settings(self.__settings_key)

    def __save(self):
        sublime.save_settings(self.__settings_key)

    def __observer_id(self, key):
        return '{}.{}'.format(self.__settings_key, key)


class FormatterSettings:
    def __init__(self, name):
        self.__name = name
        self.__cache = None
        self.__settings = Settings()
        self.__settings.add_observer(self.__name, self.__invalidate_cache)

    def __del__(self):
        self.__settings.remove_observer(self.__name)

    @property
    def format_on_save(self):
        return self.__get('format_on_save', default=False)

    @format_on_save.setter
    def format_on_save(self, value):
        return self.__set('format_on_save', value)

    @property
    def sources(self):
        return self.__get('sources', default=[])

    @property
    def options(self):
        return self.__get('options', default=[])

    def __get(self, value, default=None):
        return self.__formatter_settings().get(value, default)

    def __set(self, key, value):
        formatter_settings = self.__formatter_settings()
        formatter_settings[key] = value
        self.__settings.update_formatter(self.__name, formatter_settings)

    def __formatter_settings(self):
        if self.__cache is None:
            self.__cache = self.__settings.formatter(self.__name)
        return self.__cache

    def __invalidate_cache(self):
        self.cache = None
