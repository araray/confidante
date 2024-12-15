from __future__ import annotations
from typing import Any, Protocol

class ConfigLoader(Protocol):
    def load(self, path: str) -> dict[str, Any]:
        pass
    def dump(self, data: dict[str, Any], path: str) -> None:
        pass
