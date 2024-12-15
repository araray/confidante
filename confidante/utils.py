from typing import Any

class ConfigAccessor:
    """
    Allows both dot notation and dict notation access.
    """
    def __init__(self, data: dict[str, Any]):
        # Store a direct reference
        self._data = data

    def __getattr__(self, item):
        if item in self._data and isinstance(self._data[item], dict):
            return ConfigAccessor(self._data[item])
        elif item in self._data:
            return self._data[item]
        else:
            raise AttributeError(f"No such configuration key: {item}")

    def __getitem__(self, item):
        val = self._data[item]
        if isinstance(val, dict):
            return ConfigAccessor(val)
        return val
