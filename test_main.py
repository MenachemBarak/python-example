from pathlib import Path

from main import TodoStore, main


def test_add_done_remove(tmp_path: Path) -> None:
    db = tmp_path / "todos.json"
    assert main(["--db", str(db), "add", "Buy milk"]) == 0
    assert main(["--db", str(db), "add", "Walk dog"]) == 0
    assert main(["--db", str(db), "done", "1"]) == 0

    tasks = TodoStore(db).tasks
    assert [(t.id, t.title, t.done) for t in tasks] == [
        (1, "Buy milk", True),
        (2, "Walk dog", False),
    ]

    assert main(["--db", str(db), "remove", "1"]) == 0
    assert [t.id for t in TodoStore(db).tasks] == [2]


def test_unknown_id_returns_error(tmp_path: Path) -> None:
    assert main(["--db", str(tmp_path / "todos.json"), "done", "99"]) == 1
