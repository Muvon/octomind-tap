---
name: programming-rust
title: "Rust Development"
description: "Idiomatic Rust architecture, ownership patterns, and ecosystem choices that survive long-term maintenance. Auto-activates in Rust projects."
license: Apache-2.0
compatibility: "Requires cargo and rustc toolchain."
capabilities: programming-rust
domains: developer
rules:
  - file(Cargo.toml)
  - content(rust)
---

## Overview

Write Rust with explicit ownership, meaningful errors, and small APIs. Research baseline: stable Rust 1.98, checked 2026-09-05. Read `rust-toolchain.toml`, Cargo `edition`, `rust-version` (minimum supported Rust version, MSRV), features, and CI targets before choosing syntax or dependencies. Recheck official releases when updating; a newer compiler does not authorize raising the project's MSRV or changing its edition.

## Mental model

Make invalid states difficult to construct and make each resource's owner visible. Borrow for temporary access; own data when it must outlive the call. Choose the simplest representation that expresses the lifecycle, including a straightforward clone when independent ownership is needed.

## Version-aware choices

- Rust 2024 requires 1.85+. Edition changes can alter temporary lifetimes and pattern behavior; follow the migration guide and review generated changes separately from feature work.
- Use stable standard-library facilities supported by the MSRV before adding a crate for the same small task. Nightly features remain opt-in; don't hide missing support behind unrequested compatibility branches.
- Rust 1.98 adds integer `format_into` with `NumBuffer`, useful for measured formatting hotspots. Its floating-point `algebraic_*` methods permit reassociation and nondeterministic results; ordinary arithmetic remains appropriate when reproducibility matters.

## Ownership and APIs

- Accept `&str`, `&[T]`, and `&Path` for borrowed reads; accept owned values when the function retains or transfers them. Borrowed struct fields are useful for views with clear lifetimes, but owned fields simplify independently stored records.
- Keep items private until another module needs them; widen to `pub(crate)` or `pub` deliberately. Split crates for independent reuse, dependency boundaries, or deployment needs, not by default.
- Use enums for mutually exclusive states and newtypes for distinct domain identifiers. Keep constructors responsible for invariants; expose accessors rather than mutable fields that bypass validation.
- Introduce traits for an actual behavioral boundary, including a useful test seam. Choose generics for compile-time specialization and `dyn Trait` for runtime heterogeneity; neither is universally superior.
- Use `Rc`/`Arc` for shared ownership and a suitable synchronization primitive for mutation. Reference counting alone does not make shared mutation safe. Use `Cow` when mixed borrowing/ownership materially simplifies an API.

## Errors and effects

- Return `Result` for recoverable failures and `Option` for expected absence. Propagate with `?`; don't convert failed parsing, I/O, or configuration into an empty collection or default value unless that behavior is the documented contract.
- Use errors callers can inspect when they must recover differently. Preserve underlying causes with `Error::source`; existing `thiserror` or application context libraries can reduce boilerplate, but a new dependency is not mandatory.
- Include operation context without secrets. Add context where it becomes meaningful; log once at the boundary that handles the failure.
- Reserve `expect` for proven invariants and explain why they hold; external input is not an invariant. Use `#[non_exhaustive]` on public enums intended to grow, understanding that it requires downstream wildcard handling.
- Keep `unsafe` localized behind a safe interface, with explicit safety arguments covering aliasing, validity, lifetime, and synchronization. A passing compiler is not an unsafe-code proof.

## Async and concurrency

- Keep short, non-awaiting critical sections under a synchronous mutex when contention permits. Release its guard before `.await`; use an async mutex when holding a lock across awaits is required. Actors fit asynchronously managed resources, not every shared value.
- Bound task concurrency and queues. Own task handles and define shutdown, cancellation, and error collection; dropping a spawned-task handle need not stop its task.
- In `select!`, losing branch futures owned by the expression are dropped; borrowing an externally retained future does not drop its underlying operation. Check cancellation safety and retain partial protocol state outside cancellable futures when needed.
- Offload blocking I/O appropriately. Bound CPU-heavy blocking work or use a CPU-oriented pool; spawning unlimited blocking jobs is not backpressure.

## Example

Reject zero and malformed values instead of silently substituting a worker count:

```rust
use std::num::{NonZeroUsize, ParseIntError};

fn parse_workers(input: &str) -> Result<NonZeroUsize, ParseIntError> {
    input.parse()
}
```

## Checklist

- [ ] Syntax, dependencies, features, and targets respect the declared MSRV and edition.
- [ ] Ownership, error recovery, and cancellation preserve the intended contract.
- [ ] No unexplained clones, public surface expansion, swallowed failures, or unsafe assumptions.
- [ ] Use project formatting, Clippy, and focused tests when execution is authorized; cover failure paths and supported feature combinations. Report checks skipped.

## References

- [Rust releases](https://blog.rust-lang.org/releases/) and [1.98 changes](https://blog.rust-lang.org/2026/08/20/Rust-1.98.0/).
- [Cargo MSRV](https://doc.rust-lang.org/cargo/reference/rust-version.html) and [Rust 2024 migration](https://doc.rust-lang.org/edition-guide/rust-2024/index.html).
- [Rust API guidelines](https://rust-lang.github.io/api-guidelines/future-proofing.html), [error contract](https://doc.rust-lang.org/std/error/trait.Error.html), and [NonZero](https://doc.rust-lang.org/std/num/struct.NonZero.html).
- [Tokio shared state](https://tokio.rs/tokio/tutorial/shared-state) and [cancellation with select](https://tokio.rs/tokio/tutorial/select).
