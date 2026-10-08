from taskcli.config import load_config, DEFAULTS


def test_missing_file_gives_defaults(tmp_path):
    assert load_config(tmp_path / "none.toml") == DEFAULTS
