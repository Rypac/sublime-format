from __future__ import annotations

from enum import Enum
from sublime import active_window, error_message, Window
from typing import Optional


class ErrorStyle(Enum):
    NONE = ""
    CONSOLE = "console"
    PANEL = "panel"
    DIALOG = "dialog"


class FormatError(Exception):
    __slots__ = ["message", "style"]

    def __init__(self, message: str, style: ErrorStyle) -> None:
        self.message = message
        self.style = style

    def __str__(self) -> str:
        return self.message


def display_error(error: FormatError, window: Optional[Window] = None) -> None:
    window = window or active_window()

    if error.style == ErrorStyle.NONE:
        return

    elif error.style == ErrorStyle.CONSOLE:
        print(error)

    elif error.style == ErrorStyle.PANEL:
        panel = window.create_output_panel("Format")
        panel.settings().update({"line_numbers": False})
        panel.run_command("insert", {"characters": str(error)})
        window.run_command("show_panel", {"panel": "output.Format"})

    elif error.style == ErrorStyle.DIALOG:
        error_message(str(error))


def clear_error(window: Optional[Window] = None) -> None:
    window = window or active_window()

    window.destroy_output_panel("Format")
