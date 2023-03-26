from __future__ import annotations

from dataclasses import dataclass
from sublime import Settings
from typing import Any, Dict, List, Optional, Union


@dataclass
class Configuration:
    selector: str
    cmd: List[str]
    enabled: bool
    format_on_save: bool
    error_style: str
    timeout: int

    @staticmethod
    def create(
        settings: Union[Settings, Dict[str, Any]],
        overrides: Dict[str, Any] = {},
    ) -> Configuration:
        def setting(key: str, default: Optional[Any] = None):
            return (
                overrides.get(key) if key in overrides else settings.get(key, default)
            )

        return Configuration(
            selector=setting("selector"),
            cmd=setting("cmd"),
            enabled=setting("enabled", default=True),
            format_on_save=setting("format_on_save", default=False),
            error_style=setting("error_style", default="panel"),
            timeout=setting("timeout", default=60),
        )
