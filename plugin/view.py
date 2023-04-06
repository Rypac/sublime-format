from __future__ import annotations

from sublime import Region, View

import os


def view_region(view: View) -> Region:
    return Region(0, view.size())


def view_scope(view: View) -> str:
    scopes = view.scope_name(0)
    return scopes[0 : scopes.find(" ")]


def extract_variables(view: View) -> dict[str, str]:
    settings = view.settings()
    tab_size = settings.get("tab_size") or 0
    indent = " " * tab_size if settings.get("translate_tabs_to_spaces") else "\t"

    variables = window.extract_variables() if (window := view.window()) else {}
    variables["tab_size"] = str(tab_size)
    variables["indent"] = indent
    variables.update(os.environ)

    return variables
