import pytest
from cryptography.fernet import Fernet

@pytest.fixture
def symmetric_key():
    return Fernet.generate_key().decode('utf-8')  # or a static known key
