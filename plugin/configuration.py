from __future__ import annotations

from typing import Any, Dict, List


class Configuration(dict):
    @property
    def selector(self) -> str:
        return self.get("selector")

    @property
    def cmd(self) -> List[str]:
        return self.get("cmd")

    @property
    def enabled(self) -> bool:
        return self.get("enabled", True)

    @property
    def format_on_save(self) -> bool:
        return self.get("format_on_save", False)

    @property
    def error_style(self) -> str:
        return self.get("error_style", "panel")

    @property
    def timeout(self) -> int:
        return self.get("timeout", 60)

    @staticmethod
    def create(settings: Dict[str, Any], overrides: Dict[str, Any]) -> Configuration:
        merged = Configuration()
        for key, value in settings.items():
            if key != "formatters":
                merged[key] = value
        for key, value in overrides.items():
            if key != "formatters":
                merged[key] = value
        return merged
