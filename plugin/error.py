from __future__ import annotations

from enum import Enum
from sublime import active_window, error_message, Window
from typing import Optional


class ErrorStyle(Enum):
    NONE = ""
    CONSOLE = "console"
    PANEL = "panel"
    DIALOG = "dialog"


def display_error(
    message: str,
    window: Optional[Window] = None,
    style: ErrorStyle = ErrorStyle.CONSOLE,
) -> None:
    window = window or active_window()

    if style == ErrorStyle.NONE:
        return

    elif style == ErrorStyle.CONSOLE:
        print(message)

    elif style == ErrorStyle.PANEL:
        panel = window.create_output_panel("Format")
        panel.settings().update({"line_numbers": False})
        panel.run_command("insert", {"characters": message})
        window.run_command("show_panel", {"panel": "output.Format"})

    elif style == ErrorStyle.DIALOG:
        error_message(message)


def clear_error(window: Optional[Window] = None) -> None:
    window = window or active_window()

    window.destroy_output_panel("Format")
