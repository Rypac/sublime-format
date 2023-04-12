from __future__ import annotations

from functools import wraps
from typing import Any, Callable


def cached(cache, key, include: Callable[[str, Any], bool] | None = None):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if (instance_cache := cache(self)) is None:
                return method(self, *args, **kwargs)

            cache_key = key(*args, **kwargs)
            if cache_key in instance_cache:
                return instance_cache[cache_key]

            value = method(self, *args, **kwargs)
            if include is None or include(cache_key, value):
                try:
                    instance_cache[cache_key] = value
                except ValueError:
                    pass

            return value

        return wrapper

    return decorator
