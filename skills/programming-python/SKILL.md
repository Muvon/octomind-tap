---
name: programming-python
title: "Python Development Best Practices"
description: "Pythonic best practices for AI coding agents: architecture, type-driven design, and library choices that scale beyond scripts. Auto-activates in Python projects."
license: Apache-2.0
compatibility: "Requires the Python interpreter and environment selected by the project."
capabilities: programming-python
domains: developer
rules:
  - file(pyproject.toml)
  - file(setup.py)
  - file(setup.cfg)
  - file(requirements.txt)
  - content(python)
---

## Overview

Write Python with clear data contracts, deliberate effects, and predictable failure behavior. As of 2026-10: Python 3.15 is the newest stable release (2026-10-09), 3.14 is in bugfix, and 3.10 reached end of life on 2026-10-01. Read `requires-python`, environment pins, dependency lockfiles, type-checker settings, and CI first. Use features supported by every required interpreter; don't raise the minimum version or replace the project's tooling during unrelated work. Recheck official releases when updating this guidance.

## Mental model

Annotations describe a contract; validation enforces it. Keep boundary parsing explicit, represent trusted data with small types, and make ownership of mutable state and resources visible. A function or module is enough until a class or abstraction solves a concrete lifecycle or substitution problem.

## Recent features and migration traps

| Version | Useful change and boundary |
|---------|----------------------------|
| 3.11 | `TaskGroup`, exception groups/`except*`, and `asyncio.timeout` support structured concurrent failure handling. |
| 3.12 | `type Alias = ...` and type-parameter syntax (`def first[T](...)`) simplify typed APIs; older interpreters cannot parse them. |
| 3.13 | `TypeIs` supports narrowing both branches; use it only when its condition exactly identifies the claimed type. |
| 3.14 | Annotations are deferred by default; `annotationlib` supports introspection. T-strings produce `Template` objects, and free-threaded builds are officially supported. |
| 3.15 | `lazy import` / `lazy from ... import` at module scope (PEP 810), built-in `frozendict` (PEP 814) and `sentinel` (PEP 661), unpacking in comprehensions (`[*xs for xs in groups]`), `TaskGroup.cancel()`, TypedDict `extra_items` (PEP 728), and the `profiling.sampling` profiler that attaches to a running PID. I/O defaults to UTF-8 regardless of locale (PEP 686). |

Don't assume annotation values are eagerly evaluated or all strings. Use `typing.get_type_hints` when evaluated types are needed, or appropriate `annotationlib` formats for introspection; evaluating annotations can execute code. T-strings preserve literal and interpolated parts for a processor: they do not automatically escape HTML or parameterize SQL, and they are not interchangeable with `str`.

Lazy imports defer import errors and import-time side effects to first use; don't make a module lazy when its import registers plugins or must fail fast at startup. `frozendict` is not a `dict` subclass, so `isinstance(x, dict)` checks miss it; check `collections.abc.Mapping` where both are valid. The UTF-8 default changes behavior on Windows and non-UTF-8 locales; keep passing `encoding=` explicitly in code that supports older interpreters.

## Types and data

- Annotate public boundaries and non-obvious internal contracts; use `list[T]`, `dict[K, V]`, and `T | None` on supported versions. Use `object` for unknown data that must be narrowed; isolate necessary `Any` at untyped integration points.
- `TypedDict` describes dictionary shape without runtime validation. `Protocol` describes structural behavior; a runtime-checkable protocol does not verify method signatures or semantic correctness.
- Use dataclasses for records; choose `frozen=True` when reassignment is unwanted and `slots=True` when its restrictions fit. Frozen fields do not freeze nested lists or dictionaries. Use `default_factory` for mutable defaults.
- Validate untrusted values once at entry and pass trusted values inward. Choose strict validation or explicit coercion deliberately; don't let a serializer or modeling library quietly change the input contract.
- Use an explicit `is None` check when zero, `False`, or an empty collection is valid. Truthiness-based defaults can erase meaningful input.

## Errors, resources, and module design

- Catch specific failures close to the operation that can recover. A top-level handler may catch broadly to report failure, but should not pretend success. Add a domain exception when callers need that distinction; preserve causes with `raise ... from ...`.
- Don't replace missing required configuration, failed I/O, or invalid input with defaults. Suppress only a named, expected failure whose absence is part of the contract. Keep sensitive input out of exception messages and logs.
- Use `with`/`async with` for resources and `ExitStack` for dynamic groups. Make cleanup observable where failure matters; finalizers and garbage collection do not guarantee timely cleanup.
- Keep imports free of heavyweight work and mutable global configuration. Public submodules are valid APIs; re-exporting everything from `__init__.py` is unnecessary and can introduce cycles.
- Use `pyproject.toml` for modern package metadata and `[dependency-groups]` (PEP 735) for dev/test dependencies. A `src/` layout helps test installed-package behavior; flat layouts and requirements files still have valid uses. Preserve the established package/environment tools unless changing them is part of the task. For a new project with no established tooling, uv (`uv.lock`, `uv run`) plus Ruff for lint and format is the common default; commit the lockfile for applications.

## Concurrency

- Use async I/O for concurrent awaitable operations and threads for blocking I/O. In a GIL-enabled interpreter, pure-Python CPU work generally needs processes, isolated interpreters, or native code that releases the GIL for parallelism.
- Free-threaded builds can execute Python threads in parallel, but extensions may re-enable the GIL. Verify runtime and dependency support; protect compound shared mutations with locks rather than relying on container internals.
- `TaskGroup` cancels siblings after an ordinary task failure and waits for cleanup. Propagate `CancelledError` after necessary cleanup; swallowing it can break task groups and timeouts. `gather` has different failure semantics and remains useful when those semantics are intended.
- Keep blocking work off the event loop with appropriate executors or `to_thread`. Bound queued work; cancelling an awaiting coroutine does not necessarily stop a running thread.
- Python 3.14 no longer defaults to `fork` on any platform. Make process-pool entry points importable, guard startup with `if __name__ == "__main__":`, and explicitly choose a multiprocessing context only when required. `InterpreterPoolExecutor` provides isolated interpreters, not shared mutable globals.

## Example

A missing optional value may use a default; an invalid supplied value must fail:

```python
def parse_workers(raw: str | None) -> int:
    if raw is None:
        return 4
    try:
        workers = int(raw)
    except ValueError as exc:
        raise ValueError("worker count must be an integer") from exc
    if workers < 1:
        raise ValueError("worker count must be positive")
    return workers
```

## Checklist

- [ ] Syntax and libraries match the supported Python versions and interpreter build.
- [ ] Types are validated at boundaries; mutable defaults and truthiness don't change meaning.
- [ ] Errors, cleanup, cancellation, and worker shutdown preserve the contract.
- [ ] When authorized, use the project's formatter, linter, type checker, and focused tests. Cover invalid input and concurrent cleanup; report skipped checks without installing missing tools implicitly.

## References

- [Release status](https://www.python.org/downloads/), [Python 3.15 changes](https://docs.python.org/3.15/whatsnew/3.15.html), and [Python 3.14 changes](https://docs.python.org/3.14/whatsnew/3.14.html).
- [Typing](https://docs.python.org/3.14/library/typing.html), [dataclasses](https://docs.python.org/3.14/library/dataclasses.html), [annotation introspection](https://docs.python.org/3.14/library/annotationlib.html), and [t-strings](https://docs.python.org/3.14/library/string.templatelib.html).
- [Async task contracts](https://docs.python.org/3.14/library/asyncio-task.html), [free threading](https://docs.python.org/3.14/howto/free-threading-python.html), [multiprocessing](https://docs.python.org/3.14/library/multiprocessing.html), and [executors](https://docs.python.org/3.14/library/concurrent.futures.html).
- [uv project workflow](https://docs.astral.sh/uv/) and [PyPA layout tradeoffs](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
