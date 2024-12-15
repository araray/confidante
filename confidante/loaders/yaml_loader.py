import yaml
from typing import Any
from .base import ConfigLoader

class YamlLoader:
    def load(self, path: str) -> dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def dump(self, data: dict[str, Any], path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=True)
