from __future__ import annotations

from sublime import Region, View


def view_region(view: View) -> Region:
    return Region(0, view.size())


def view_scope(view: View) -> str:
    scopes = view.scope_name(0)
    return scopes[0 : scopes.find(" ")]
