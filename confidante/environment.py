import os
from typing import Any

def merge_env(config: dict[str, Any], prefix: str="CONFIDANTE") -> dict[str, Any]:
    # Map ENV variables in form: CONFIDANTE__SECTION__KEY=value
    # to config["section"]["key"] = value
    env = os.environ
    result = config.copy()

    for k, v in env.items():
        if k.startswith(prefix + "__"):
            path = k[len(prefix + "__"):].split("__")
            _set_path(result, path, v)
    return result

def _set_path(d: dict[str, Any], path: list[str], value: str):
    curr = d
    for p in path[:-1]:
        if p not in curr or not isinstance(curr[p], dict):
            curr[p] = {}
        curr = curr[p]
    curr[path[-1]] = value
