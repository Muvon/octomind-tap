---
name: programming-python
title: "Python Development"
description: "Pythonic architecture, type-driven design, and library choices that scale beyond scripts. Auto-activates in Python projects."
license: Apache-2.0
compatibility: "Requires Python 3.10+."
capabilities: programming-python
domains: developer
rules:
  - file(pyproject.toml)
  - file(setup.py)
  - file(setup.cfg)
  - file(requirements.txt)
  - content(python)
---

## Mental model

Python is dynamic but reads best when written as if it were typed. The cost of "just a script" compounds quickly — pick a layout, type annotations, and a data-modeling library on day one. Most maintenance pain comes from `dict`-based data flying through call chains and from mutable global state.

## Type-driven design

- Annotate every public function signature and dataclass field — types are documentation that the type checker enforces
- Model data with `dataclass(frozen=True, slots=True)` for plain records; `pydantic.BaseModel` when you need validation, coercion, or serialization at boundaries
- `TypedDict` for dicts that cross module boundaries; `Protocol` for structural interfaces ("anything with `.read()`")
- Prefer `X | None` over an implicit `None` default; explicit optionals catch the forgotten check
- Treat `Any` as a code smell — `object` plus a narrowing `isinstance` is almost always better

## Architecture

- Module boundaries reflect data flow, not file size — one module per cohesive concern (parsing, persistence, transport)
- Dependency direction goes inward: domain logic must not import from web/CLI/DB layers; inject those via callables or protocols
- Pure functions in the core, side effects at the edge — makes testing trivial and refactoring safe
- A package's `__init__.py` declares the public surface (`__all__`) and re-exports it; consumers should never reach into submodules
- Avoid singletons and module-level mutable state; configuration is a value passed in, not a global to mutate

## Async and concurrency

- Pick one model per process: `asyncio` for I/O-bound, `multiprocessing` / `concurrent.futures` for CPU-bound, threads only for blocking C extensions
- Don't mix sync and async libraries in an async path (`requests` inside `async def` blocks the loop — use `httpx.AsyncClient`)
- `asyncio.TaskGroup` (3.11+) for structured concurrency; falling back to `gather` requires explicit cancellation handling
- CPU work in an async program goes through `asyncio.to_thread` or a process pool — never inline
- The GIL means threads don't speed up Python code; use them for I/O wait or to call into release-the-GIL native libraries

## Error handling

- Define a small exception hierarchy rooted at one base class per package — callers catch the base, you add specific subclasses freely
- Raise specific, never bare `Exception`; catch specific, never bare `except:`
- Exceptions carry context — include the offending value in the message, use `raise NewError(...) from original` to preserve the chain
- Use `contextlib.suppress` for genuinely intentional ignores; an empty `except` block is a bug

## Standard library first

- `pathlib.Path` for filesystem work; `os.path` is legacy
- `dataclasses`, `enum`, `functools` (cache, partial, reduce), `itertools` (chain, groupby, islice)
- `contextlib` (contextmanager, ExitStack, suppress) — write your own context managers freely
- `logging` with `logger = logging.getLogger(__name__)` per module; configure once at the entry point, never `print` for diagnostics

## Ecosystem defaults

- Project + envs: `uv` (`uv init`, `uv add`, `uv run`) — replaces pip/poetry/venv
- HTTP: `httpx` (sync and async share the same API)
- Web: `FastAPI` for APIs, `Starlette` for raw ASGI, `Django` for batteries-included apps
- Data validation at boundaries: `pydantic` v2
- Testing: `pytest` with fixtures and `parametrize`; `hypothesis` for property tests
- CLI: `typer` (type-hint-driven) or `click`
- Background work: `arq`, `dramatiq`, or `celery` depending on scale

## Project layout

- `src/<package>/` layout from day one — prevents accidentally importing local files instead of the installed package during tests
- All metadata in `pyproject.toml`; no `setup.py`, no `requirements.txt` for new projects
- One package per repo for a library; a service may have multiple packages but one top-level entry point
- Tests in `tests/` mirroring the package structure; integration vs unit by directory, not by marker alone
