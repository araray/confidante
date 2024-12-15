from __future__ import annotations
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
import base64
from typing import Optional
from .base import CryptoBackend

class AsymmetricCrypto(CryptoBackend):
    def __init__(self, private_key_path: str, passphrase: Optional[str] = None):
        with open(private_key_path, "rb") as key_file:
            self._private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=passphrase.encode('utf-8') if passphrase else None
            )
        if not isinstance(self._private_key, rsa.RSAPrivateKey):
            raise ValueError("Private key must be RSA.")
        self._public_key = self._private_key.public_key()

    def encrypt(self, value: str) -> str:
        ciphertext = self._public_key.encrypt(
            value.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return "ENC::" + base64.urlsafe_b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext: str) -> str:
        data = base64.urlsafe_b64decode(ciphertext)
        decrypted = self._private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')
