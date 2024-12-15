import pytest
from confidante.core import Confidante
from confidante.exceptions import ConfidanteError

def test_load_nonexistent():
    with pytest.raises(ConfidanteError):
        Confidante.load("nonexistent.json")

def test_basic_access(tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"something":{"some_key":"some_value"}}', encoding="utf-8")
    config = Confidante.load(str(p))
    assert config.config.something.some_key == "some_value"
    assert config.config["something"]["some_key"] == "some_value"
