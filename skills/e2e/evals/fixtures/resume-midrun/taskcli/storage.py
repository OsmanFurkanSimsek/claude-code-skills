"""Storage layer: load/save the task list as a JSON array."""
import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".taskcli" / "tasks.json"


def load_tasks(path: Path = DEFAULT_PATH) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise ValueError(f"Corrupt task file: {path}")
    if not isinstance(data, list):
        raise ValueError(f"Task file is not a JSON array: {path}")
    return data


def save_tasks(tasks: list[dict], path: Path = DEFAULT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
