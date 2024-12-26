import os
import json
import pytest
from click.testing import CliRunner
from confidante.cli import main
from confidante.core import Confidante
from cryptography.fernet import Fernet

@pytest.fixture
def symmetric_key():
    # Example symmetric key
    return "F9i1HXS-EpWUZRNI1Sg3nhYnPomN6r5rLhJCRoZcwv8="

@pytest.fixture
def encrypted_config(tmp_path, symmetric_key):
    # Create a config file with an encrypted value
    # Encrypt a value manually here for testing
    f = Fernet(symmetric_key.encode('utf-8'))
    enc_value = f.encrypt(b"supersecret")
    enc_str = "ENC::" + Fernet.generate_key().decode()  # fake, for demonstration
    # Actually encrypt:
    enc_str = "ENC::" + f.encrypt(b"supersecret").decode('utf-8')

    config_path = tmp_path / "encrypted.json"
    data = {
        "credentials": {
            "api_key": enc_str
        }
    }
    config_path.write_text(json.dumps(data), encoding="utf-8")
    return str(config_path)

def test_integration_unlock_and_load(encrypted_config, symmetric_key):
    # Load and unlock using the provided key
    config = Confidante.load(encrypted_config)
    config.unlock(key=symmetric_key)
    assert config.config.credentials.api_key == "supersecret"

def test_cli_load_decrypted(encrypted_config, symmetric_key, monkeypatch):
    monkeypatch.setenv("CONFIDANTE_KEY", symmetric_key)
    print("AV#01: ", os.getenv("CONFIDANTE_KEY"))
    runner = CliRunner()
    result = runner.invoke(main, ["load", encrypted_config, "--decrypted"])
    print("AV#02: ", result.output)
    assert result.exit_code == 0
    assert "supersecret" in result.output

def test_tidy_json(tmp_path):
    config_path = tmp_path / "untidy.json"
    # Unsorted keys
    data = {
        "z": 1,
        "a": 2,
        "m": {"c": 3, "b": 4}
    }
    config_path.write_text(json.dumps(data), encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["tidy", str(config_path)])
    assert result.exit_code == 0
    # Reload and check if sorted
    conf = Confidante.load(str(config_path))
    keys = list(conf.config._data.keys())
    assert keys == ["a", "m", "z"]
    mk = list(conf.config.m._data.keys())
    assert mk == ["b", "c"]
