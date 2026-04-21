---
name: programming-python
title: "Python Development"
description: "Python conventions, type hints, modern tooling (uv, ruff, mypy, pytest), and best practices. Auto-activates in Python projects."
license: Apache-2.0
compatibility: "Requires Python 3.10+ and uv."
capabilities: programming-python
domains: developer
rules:
  - file(pyproject.toml)
  - file(setup.py)
  - file(setup.cfg)
  - file(requirements.txt)
  - content(python)
---

# Python Development

## Conventions

- Idiomatic Python — follow PEP 8, PEP 20, and community conventions
- Type hints everywhere — annotate all functions, methods, and variables
- Strict mypy — target `mypy --strict` compliance
- Ruff for linting and formatting — replaces flake8, isort, black
- pytest for testing — fixtures, parametrize, markers
- uv for dependency management — fast, modern, replaces pip/venv
- Dataclasses and Pydantic — prefer over raw dicts for structured data
- Pathlib over os.path — always use `pathlib.Path`

## Type System

- `from __future__ import annotations` for forward references
- Prefer `X | Y` over `Union[X, Y]` (Python 3.10+)
- Use `TypeVar`, `Generic`, `Protocol` for advanced typing
- Never use `Any` unless absolutely unavoidable — use `object` instead
- Use `TypedDict` for typed dicts, `NamedTuple` for tuples
- PHPDoc-style type comments are NOT acceptable — use annotations

## Error Handling

- Use specific exceptions — never bare `except:`
- Create custom exception hierarchies for libraries
- Use `contextlib.suppress()` for intentional suppression
- Provide context in exception messages
- Use `ExceptionGroup` (Python 3.11+) for multiple errors

## Async Patterns

- `asyncio` for I/O-bound concurrency
- `async def` / `await` — never mix sync and async carelessly
- Use `asyncio.gather()` for parallel async tasks
- Use async context managers and async iterators
- `httpx` for async HTTP (not `requests`)
- Never block the event loop — use `run_in_executor` for CPU work

## Data & Collections

- Prefer list/dict/set comprehensions over `map`/`filter`
- Use `itertools` and `functools` — don't reinvent
- `dataclasses` for simple data containers
- Pydantic for validated, serializable models
- Use `slots=True` in dataclasses for memory efficiency
- Prefer `tuple` over `list` for immutable sequences

## Testing

- pytest — not unittest
- Fixtures for setup/teardown (`conftest.py`)
- `@pytest.mark.parametrize` for data-driven tests
- `pytest-cov` for coverage
- Use `hypothesis` for property-based testing
- Mock with `pytest-mock` (`mocker` fixture)
- Tests in `tests/` directory, mirroring `src/` structure

## Dependencies & Packaging

- uv for everything: `uv init`, `uv add`, `uv run`, `uv sync`
- `pyproject.toml` — single source of truth
- Pin versions in `uv.lock` for reproducibility
- Separate dev dependencies: `uv add --dev pytest ruff mypy`
- Use optional dependency groups for extras

## Code Organization

- `src/` layout for packages (`src/mypackage/`)
- `__init__.py` exposes public API only
- One class/module per file when >150 lines
- Use `__all__` to define public API
- `pyproject.toml` for all project metadata (no `setup.py`)

## Performance

- Profile before optimizing — cProfile, py-spy
- Use generators for large sequences (memory efficiency)
- `functools.lru_cache` / `functools.cache` for memoization
- numpy/pandas for numerical work — never pure Python loops on arrays
- Use `__slots__` for memory-critical classes

## Tooling

| Command | Purpose |
|---------|---------|
| `uv run python` | Run scripts in project env |
| `uv run pytest` | Run tests |
| `uv run ruff check .` | Lint |
| `uv run ruff format .` | Format |
| `uv run mypy src/` | Type check |
| `uv add <pkg>` | Add dependency |
| `uv sync` | Sync environment |
| `uv build` | Build distribution |
