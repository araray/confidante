from __future__ import annotations
from cryptography.fernet import Fernet
import base64
from .base import CryptoBackend

class SymmetricCrypto(CryptoBackend):
    def __init__(self, key: str):
        # key should be 32 url-safe base64 bytes. If not, derive a Fernet key somehow.
        # For simplicity, assume user provides a fernet key. Otherwise, we might need a KDF.
        if len(key) != 44:  # length of base64-encoded 32 bytes
            # Derive a key from user input if needed
            derived_key = base64.urlsafe_b64encode(key.encode('utf-8').ljust(32, b'0'))
            self._fernet = Fernet(derived_key)
        else:
            self._fernet = Fernet(key.encode('utf-8'))

    def encrypt(self, value: str) -> str:
        token = self._fernet.encrypt(value.encode('utf-8'))
        return "ENC::" + token.decode('utf-8')

    def decrypt(self, ciphertext: str) -> str:
        token = ciphertext.encode('utf-8')
        return self._fernet.decrypt(token).decode('utf-8')
