"""A tiny to-do list CLI backed by a JSON file.

Usage:
    uv run main.py add "Buy milk"
    uv run main.py list
    uv run main.py done 1
    uv run main.py remove 1
    uv run main.py clear
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_DB = Path.home() / ".python-example-todos.json"
TRACE_ID = uuid.uuid4().hex[:8]

logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s [%(levelname)s] [trace={TRACE_ID}] %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("todo")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


class TodoStore:
    """Loads and saves tasks to a JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.tasks: list[Task] = self._load()

    def _load(self) -> list[Task]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task(**item) for item in data]

    def save(self) -> None:
        self.path.write_text(
            json.dumps([asdict(t) for t in self.tasks], indent=2), encoding="utf-8"
        )
        log.info("saved %d task(s) to %s", len(self.tasks), self.path)

    def add(self, title: str) -> Task:
        next_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(id=next_id, title=title)
        self.tasks.append(task)
        return task

    def find(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"no task with id {task_id}")

    def complete(self, task_id: int) -> Task:
        task = self.find(task_id)
        task.done = True
        return task

    def remove(self, task_id: int) -> Task:
        task = self.find(task_id)
        self.tasks.remove(task)
        return task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple to-do list")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="JSON file path")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("add", help="add a task").add_argument("title")
    sub.add_parser("list", help="list tasks")
    sub.add_parser("done", help="mark a task done").add_argument("id", type=int)
    sub.add_parser("remove", help="delete a task").add_argument("id", type=int)
    sub.add_parser("clear", help="delete all tasks")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = TodoStore(args.db)
    log.info("command=%s db=%s", args.command, args.db)

    try:
        if args.command == "add":
            task = store.add(args.title)
            print(f"Added #{task.id}: {task.title}")
        elif args.command == "list":
            if not store.tasks:
                print("No tasks yet.")
            for t in store.tasks:
                print(f"[{'x' if t.done else ' '}] #{t.id} {t.title}")
            return 0
        elif args.command == "done":
            print(f"Completed #{store.complete(args.id).id}")
        elif args.command == "remove":
            print(f"Removed #{store.remove(args.id).id}")
        elif args.command == "clear":
            store.tasks.clear()
            print("All tasks cleared.")
    except KeyError as exc:
        log.error("%s", exc.args[0])
        return 1

    store.save()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
