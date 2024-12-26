from __future__ import annotations
from typing import Any, Optional, Union
import os
import getpass
from pathlib import Path

from .loaders.base import ConfigLoader
from .loaders.json_loader import JsonLoader
from .loaders.toml_loader import TomlLoader
from .loaders.yaml_loader import YamlLoader
from .crypto.base import CryptoBackend
from .crypto.symmetric import SymmetricCrypto
from .crypto.asymmetric import AsymmetricCrypto
from .environment import merge_env
from .utils import ConfigAccessor
from .exceptions import ConfidanteError
from .tidy import tidy_data

class Confidante:
    def __init__(self, data: dict[str, Any], path: str, loader: ConfigLoader, crypto_backend: Optional[CryptoBackend]=None):
        self._data = data
        self._path = path
        self._loader = loader
        self._crypto_backend = crypto_backend
        self._unlocked = False
        self.config = ConfigAccessor(self._data)

    @classmethod
    def load(cls, path: str, merge_env_vars: bool=False) -> Confidante:
        path_obj = Path(path)
        if not path_obj.exists():
            raise ConfidanteError(f"Config file not found: {path}")
        # Determine loader
        if path_obj.suffix == ".json":
            loader = JsonLoader()
        elif path_obj.suffix == ".toml":
            loader = TomlLoader()
        elif path_obj.suffix in [".yml", ".yaml"]:
            loader = YamlLoader()
        else:
            raise ConfidanteError("Unsupported file format.")

        data = loader.load(path)

        if merge_env_vars:
            data = merge_env(data)

        return cls(data=data, path=path, loader=loader, crypto_backend=None)

    def unlock(self, key: Optional[str] = None, passphrase: Optional[str] = None,
            private_key_path: Optional[str] = None, prompt: bool = False) -> None:
        if self._unlocked:
            return

        # Determine crypto backend if key or private_key_path is provided
        if private_key_path is not None:
            # Asymmetric mode
            backend = AsymmetricCrypto(private_key_path=private_key_path, passphrase=passphrase)
        else:
            # Symmetric mode
            if key is None:
                key = os.environ.get("CONFIDANTE_KEY")
            elif key is None and prompt:
                key = getpass.getpass("Enter decryption key: ")
            elif key is None:
                raise ConfidanteError("No key provided for symmetric decryption.")
            backend = SymmetricCrypto(key)

        # Even if there are no encrypted values, we still set the backend.
        self._crypto_backend = backend

        # If there are encrypted values, decrypt them now.
        if self._has_encrypted_values(self._data):
            self._decrypt_data(self._data, backend)

        self._unlocked = True

    def save(self) -> None:
        self._loader.dump(self._data, self._path)

    def tidy(self) -> None:
        cleaned = tidy_data(self._data)
        self._data = cleaned
        self.save()

    def encrypt_value(self, key_path: list[str], value: str) -> None:
        if not self._crypto_backend:
            raise ConfidanteError("Configuration not unlocked or no crypto backend available.")
        encrypted = self._crypto_backend.encrypt(value)
        self._set_nested_value(key_path, encrypted)

    def _set_nested_value(self, keys: list[str], value: Any) -> None:
        d = self._data
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    @staticmethod
    def _has_encrypted_values(data: Any) -> bool:
        if isinstance(data, dict):
            for v in data.values():
                if Confidante._has_encrypted_values(v):
                    return True
        elif isinstance(data, list):
            for i in data:
                if Confidante._has_encrypted_values(i):
                    return True
        elif isinstance(data, str):
            if data.startswith("ENC::"):
                return True
        return False

    def _decrypt_data(self, data: Any, backend: CryptoBackend) -> Any:
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = self._decrypt_data(v, backend)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                data[i] = self._decrypt_data(v, backend)
        elif isinstance(data, str) and data.startswith("ENC::"):
            ciphertext = data[len("ENC::"):]
            return backend.decrypt(ciphertext)
        return data
