from __future__ import annotations
from typing import Protocol

class CryptoBackend(Protocol):
    def encrypt(self, value: str) -> str:
        pass
    def decrypt(self, ciphertext: str) -> str:
        pass
