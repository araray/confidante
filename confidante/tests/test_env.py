import os
import pytest
from confidante.core import Confidante

def test_env_overrides(tmp_path, monkeypatch):
    # copy env_overrides.json into tmp_path
    config_path = tmp_path / "env_overrides.json"
    config_path.write_text('{"service":{"url":"http://localhost:8000","debug":false}}', encoding="utf-8")

    # Set environment variable to override debug
    monkeypatch.setenv("CONFIDANTE__service__debug", "true")

    conf = Confidante.load(str(config_path), merge_env_vars=True)
    print(conf.config._data)
    assert conf.config.service.debug == "true"  # note: env vars produce strings
