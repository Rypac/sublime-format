from functools import wraps


def cache(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '__cached_values'):
            self.__cached_values = {}

        key = fn.__name__
        value = self.__cached_values.get(key)
        if value is None:
            value = fn(self, *args, **kwargs)
            self.__cached_values[key] = value
        return value

    return wrapper


def recache(fn):
    @wraps(fn)
    def wrapper(self, value, *args, **kwargs):
        key = fn.__name__
        self.__cached_values[key] = value
        fn(self, value, *args, **kwargs)

    return wrapper
