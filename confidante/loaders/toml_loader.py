import sys
import tomli_w
from typing import Any
from .base import ConfigLoader

if sys.version_info >= (3,11):
    import tomllib
else:
    import tomli as tomllib

try:
    import tomli_w
except ImportError:
    # If tomli_w is not installed, consider requiring it or fallback
    raise ImportError("tomli_w not installed. Please install tomli_w for TOML writing.")

class TomlLoader:
    def load(self, path: str) -> dict[str, Any]:
        with open(path, "rb") as f:
            return tomllib.load(f)

    def dump(self, data: dict[str, Any], path: str) -> None:
        with open(path, "wb") as f:
            f.write(tomli_w.dump(data, f))
