import pytest
from click.testing import CliRunner
from confidante.cli import main


def test_cli_load(tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"a":1}', encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["load", str(p)])
    assert result.exit_code == 0
    assert '"a": 1' in result.output
