import json
import pytest
from taskcli.storage import load_tasks, save_tasks


def test_load_missing_file_returns_empty(tmp_path):
    assert load_tasks(tmp_path / "none.json") == []


def test_roundtrip(tmp_path):
    p = tmp_path / "tasks.json"
    tasks = [{"id": 1, "title": "buy milk", "done": False}]
    save_tasks(tasks, p)
    assert load_tasks(p) == tasks


def test_corrupt_file_raises(tmp_path):
    p = tmp_path / "tasks.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_tasks(p)


def test_non_array_raises(tmp_path):
    p = tmp_path / "tasks.json"
    p.write_text(json.dumps({"a": 1}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_tasks(p)
