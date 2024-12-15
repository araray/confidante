import pytest
from confidante.core import Confidante
from confidante.loaders.json_loader import JsonLoader
from confidante.loaders.toml_loader import TomlLoader
from confidante.loaders.yaml_loader import YamlLoader

def test_load_toml(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text("""
[app]
name = "test_app"
[app.settings]
theme = "dark"
timeout = 30
    """, encoding="utf-8")
    conf = Confidante.load(str(config_path))
    assert conf.config.app.name == "test_app"
    assert conf.config["app"]["settings"]["theme"] == "dark"

def test_load_yaml(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("""
app:
  name: "test_app_yaml"
  settings:
    theme: "light"
    timeout: 60
    """, encoding="utf-8")
    conf = Confidante.load(str(config_path))
    assert conf.config.app.name == "test_app_yaml"
    assert conf.config.app.settings.timeout == 60
