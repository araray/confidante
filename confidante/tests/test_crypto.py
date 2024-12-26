import json
from click.testing import CliRunner
from confidante.cli import main
from confidante.core import Confidante
from confidante.crypto.symmetric import SymmetricCrypto

def test_symmetric_crypto():
    key = "mysecretkey"
    crypto = SymmetricCrypto(key)
    enc = crypto.encrypt("hello")
    assert enc.startswith("ENC::")
    dec = crypto.decrypt(enc[len("ENC::"):])
    assert dec == "hello"

def test_cli_encrypt_key(tmp_path, symmetric_key, monkeypatch):
    config_path = tmp_path / "test_config.json"
    config_data = {"secret": "plainvalue"}
    config_path.write_text(json.dumps(config_data), encoding="utf-8")

    monkeypatch.setenv("CONFIDANTE_KEY", symmetric_key)
    runner = CliRunner()

    # Encrypt secret using CLI
    result = runner.invoke(main, ["encrypt-key", "--key", symmetric_key, str(config_path), "secret", "newsecret"])
    assert result.exit_code == 0

    # Check file now has ENC::
    updated = json.loads(config_path.read_text(encoding="utf-8"))
    assert updated["secret"].startswith("ENC::")

    # Now load and unlock
    conf = Confidante.load(str(config_path))
    conf.unlock(key=symmetric_key)
    assert conf.config.secret == "newsecret"
