from __future__ import annotations

from dataclasses import dataclass
from sublime import Settings
from typing import Dict, List, Optional


@dataclass
class Configuration:
    selector: str
    cmd: List[str]
    enabled: bool
    format_on_save: bool
    error_style: str
    timeout: int


def create_configuration(
    settings: Settings,
    formatter_settings: Dict[str, Any],
) -> Configuration:
    def setting(key: str, default: Optional[Any] = None):
        return (
            formatter_settings.get(key)
            if key in formatter_settings
            else settings.get(key, default)
        )

    return Configuration(
        selector=setting("selector"),
        cmd=setting("cmd"),
        enabled=setting("enabled", default=True),
        format_on_save=setting("format_on_save", default=False),
        error_style=setting("error_style", default="panel"),
        timeout=setting("timeout", default=60),
    )
