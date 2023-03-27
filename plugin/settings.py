from __future__ import annotations

from contextlib import contextmanager
from sublime import Settings
from sublime import load_settings, save_settings


@contextmanager
def edit_settings(name: str) -> Settings:
    settings = load_settings(name)
    yield settings
    save_settings(name)
