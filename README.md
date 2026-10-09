# python-example

A small (~100 lines) to-do list CLI written in Python and managed with [uv](https://docs.astral.sh/uv/).
It uses only the standard library and keeps tasks in a JSON file.

## Usage

```bash
uv run main.py add "Buy milk"
uv run main.py add "Walk dog"
uv run main.py done 1
uv run main.py list
uv run main.py remove 2
uv run main.py clear
```

Tasks are stored in `~/.python-example-todos.json`. Use `--db path/to/file.json` to pick a different file.

## Tests

```bash
uv run pytest
```
