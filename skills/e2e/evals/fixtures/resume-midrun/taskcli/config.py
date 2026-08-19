"""Config loader: read ~/.taskcli/config.toml with defaults. (Step 2 - in progress)"""
import tomllib
from pathlib import Path

DEFAULTS = {"color": True, "date_format": "%Y-%m-%d"}
DEFAULT_PATH = Path.home() / ".taskcli" / "config.toml"


def load_config(path: Path = DEFAULT_PATH) -> dict:
    if not path.exists():
        return dict(DEFAULTS)
    with path.open("rb") as f:
        user = tomllib.load(f)
    return {**DEFAULTS, **user}
