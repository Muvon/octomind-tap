---
name: programming-rust
title: "Rust Development"
description: "Rust conventions, idiomatic patterns, cargo tooling, and best practices. Auto-activates in Rust projects with Cargo.toml."
license: Apache-2.0
compatibility: "Requires cargo and rustc toolchain."
capabilities: programming-rust
domains: developer
rules:
  - file(Cargo.toml)
  - content(rust)
---

# Rust Development

## Conventions

- Idiomatic Rust — follow Rust conventions and community best practices
- Ownership & borrowing — leverage Rust's memory safety guarantees, prefer references over cloning
- Zero-cost abstractions — use iterators, closures, generics effectively
- Error handling — use `Result<T, E>` and `?` operator, never `.unwrap()` in production code
- Safety first — minimize `unsafe` blocks, document invariants with `/// # Safety` when necessary
- Clippy compliance — all code should pass `cargo clippy` without warnings
- rustfmt — always format code with `cargo fmt`
- Documentation — document public APIs with `///` doc comments

## Code Organization

- `lib.rs` for library code, `main.rs` for binaries
- `mod.rs` for module directories (or inline `module_name.rs` alongside directory)
- One struct/trait per file when >100 lines
- Use `pub mod` for public module exports, keep internal modules private
- Workspace (`Cargo.toml` with `[workspace]`) for multi-crate projects

## Error Handling

- `thiserror` for library errors — derive `Error` with `#[error("...")]`
- `anyhow` for application errors — `anyhow::Result` + `.context("...")`
- Implement `std::error::Error` for custom error types
- Provide context with `.context()` or `.with_context(|| ...)`
- Never use `.unwrap()` or `.expect()` in library code — return `Result`
- Use `?` operator for propagation, not explicit `match` on every error

## Performance

- Prefer iterators over indexed loops — iterators optimize better
- Use `Cow<str>` / `Cow<[T]>` to avoid unnecessary cloning
- `Arc<T>` for shared ownership across threads, `Rc<T>` for single-threaded
- Use `&'static str` for compile-time strings, avoid `String` when possible
- Benchmark before optimizing — `cargo bench` with criterion
- Preallocate with `Vec::with_capacity()` when size is known

## Safety

- Minimize `unsafe` blocks — prefer safe abstractions
- Document safety invariants: `/// # Safety` section explaining why it's sound
- Use `RefCell<T>` for interior mutability when safe
- Prefer safe abstractions (`std::sync::Mutex`, `RwLock`) over raw pointers
- Use `#[repr(C)]` only for FFI types

## Testing

- `#[test]` for unit tests, `#[cfg(test)] mod tests` at bottom of file
- Use `assert!`, `assert_eq!`, `assert_ne!` with descriptive messages
- Property-based testing with `proptest` for complex invariants
- Integration tests in `tests/` directory (separate compilation unit)
- Use `#[should_panic]` for testing error paths
- `cargo test -- --nocapture` to see println output in tests

## Dependencies

- Keep `Cargo.toml` organized: `[dependencies]`, `[dev-dependencies]`, `[build-dependencies]`
- Use workspace for multi-crate projects — shared dependency versions
- Pin versions for reproducible builds
- Review dependencies for security: `cargo audit`
- Prefer well-maintained crates with strong type safety

## Async Rust

- `tokio` or `async-std` as runtime — pick one, be consistent
- `async fn` returns `impl Future` — understand the lifetime implications
- Use `tokio::spawn` for concurrent tasks, `tokio::join!` for parallel await
- Never block the async runtime — use `spawn_blocking` for CPU work
- `Pin<Box<dyn Future>>` for trait objects returning futures
- Cancel safety: understand that dropping a future cancels it

## Tooling

| Command | Purpose |
|---------|---------|
| `cargo build` | Compile the project |
| `cargo test` | Run all tests |
| `cargo clippy` | Lint with clippy |
| `cargo fmt` | Format code |
| `cargo check` | Fast compile check (no codegen) |
| `cargo doc --open` | Generate and view documentation |
| `cargo bench` | Run benchmarks |
| `cargo audit` | Security audit dependencies |
| `cargo update` | Update dependencies |
