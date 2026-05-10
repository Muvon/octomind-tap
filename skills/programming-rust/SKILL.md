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

## Mental model

Rust pushes design decisions to compile time. Most "Rust pain" comes from fighting the borrow checker after a bad architectural choice — usually shared mutable state that should have been ownership transfer, an actor, or a channel. Design data flow first; lifetimes and clones fall out cleanly when ownership is clear.

## Ownership and data flow

- Default to owned types in struct fields (`String`, `Vec<T>`, `PathBuf`) — borrowed fields force lifetime parameters that infect every caller
- Borrow in function signatures: take `&str` / `&[T]` / `&Path`, return owned values; callers decide when to clone
- Reach for `Cow<'a, T>` only when measurement shows allocation pressure — premature `Cow` costs more in API complexity than it saves
- Interior mutability (`RefCell`, `Mutex`) is a signal the design has shared state — first ask whether ownership transfer or message passing fits
- `Arc<Mutex<T>>` held across `.await` is a deadlock waiting to happen — prefer `tokio::sync::Mutex`, an actor with a channel, or splitting the state

## Error design

- One error enum per crate boundary, derived with `thiserror`; variants describe the failure domain, not the underlying cause
- Convert foreign errors at the boundary with `#[from]` — don't let `std::io::Error` leak through every layer
- Applications wrap with `anyhow::Context` at the call site where context is meaningful, not at function definitions
- Errors are part of the API — adding a variant is a breaking change; use `#[non_exhaustive]` from day one

## Traits and abstraction

- Define a trait when there are two real implementations, not in anticipation; generics are easy to add, hard to remove
- Static dispatch (`fn f<T: Trait>`) is the default; `Box<dyn Trait>` only when the type must be erased (heterogeneous collections, plugin boundaries)
- Keep traits small and orthogonal — `Read`, `Write`, `Iterator` are the model; avoid god traits
- Newtype pattern (`struct UserId(u64)`) for domain types — prevents mixing semantically different primitives

## Async architecture

- Pick one runtime per binary; libraries should stay runtime-agnostic where possible or feature-gate the runtime
- Model long-lived state as actors: a task owns the state, others send messages over `mpsc`/`oneshot` — eliminates `Arc<Mutex<_>>`
- `tokio::select!` for cancellation and multiplexing; ensure each branch is cancel-safe (no half-applied mutation across awaits)
- CPU work belongs in `spawn_blocking` or `rayon`, never on the async runtime
- Backpressure is the caller's responsibility — bounded channels and limited streams, not unbounded queues

## Module and crate layout

- One concept per module; module names are nouns, not verbs (`parser`, not `parsing`)
- Workspace from the start for anything non-trivial — split by deployment unit (binary, lib, proc-macro), not by layer
- `pub(crate)` is the default visibility for internal items; `pub` only for the deliberate API surface
- Re-export at the crate root what consumers need; don't force them to navigate the internal module tree

## Testing approach

- Unit tests live in `#[cfg(test)] mod tests` next to the code they exercise
- Integration tests in `tests/` exercise the public API as an external consumer would — they catch accidental API breakage
- Property tests (`proptest`, `quickcheck`) for parsers, codecs, and anything with algebraic invariants
- `insta` for snapshot tests on rendered output (errors, generated code, serialized formats)

## Ecosystem defaults

- Serialization: `serde` with `serde_json` / `bincode` / `toml`
- HTTP server: `axum` or `actix-web`; client: `reqwest`
- Database: `sqlx` (compile-checked queries) or `diesel` (typed query builder)
- CLI: `clap` with derive macros
- Observability: `tracing` + `tracing-subscriber` — structured spans beat `log` for async code
