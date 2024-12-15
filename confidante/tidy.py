from typing import Any, Union

def tidy_data(data: Any) -> Any:
    # For JSON, just ensure sorted keys
    if isinstance(data, dict):
        # Sort keys recursively
        return {k: tidy_data(data[k]) for k in sorted(data.keys())}
    elif isinstance(data, list):
        return [tidy_data(i) for i in data]
    else:
        return data
