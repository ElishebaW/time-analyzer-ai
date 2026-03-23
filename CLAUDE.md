# Claude Code Guidelines

## Linting and Formatting

This project uses [Ruff](https://docs.astral.sh/ruff/) 0.15.7 for linting and formatting (replacing black, isort, and flake8).

All Python files must pass Ruff before committing. Run the following to check:

```bash
uv run ruff check
uv run ruff format --check
```

To auto-fix issues:

```bash
uv run ruff check --fix
uv run ruff format
```

Ruff is configured in `pyproject.toml` under `[tool.ruff]`. Key settings:
- Line length: 88
- Selected rules: `E` (pycodestyle), `F` (Pyflakes), `I` (isort), `UP` (pyupgrade)
- `E501` (line too long) is ignored for `analyze_api.py` and `analyze_time.py` due to intentional long LLM prompt strings
