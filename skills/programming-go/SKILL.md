---
name: programming-go
title: "Go Development"
description: "Idiomatic Go architecture, concurrency design, and standard-library-first patterns. Auto-activates in Go projects."
license: Apache-2.0
compatibility: "Requires Go toolchain (go 1.21+)."
domains: developer
rules:
  - file(go.mod)
  - content(golang)
---

## Mental model

Go optimizes for code that ten people can maintain for ten years. Simplicity, explicitness, and a small standard vocabulary matter more than cleverness. Resist the urge to import patterns from Java, Ruby, or TypeScript — interfaces, generics, and inheritance hierarchies that feel natural elsewhere produce unidiomatic Go.

## Architecture

- Package boundaries reflect capabilities, not layers — `auth`, `billing`, `inventory`, not `controllers`/`services`/`repositories`
- Define interfaces in the consuming package, not where the type that implements them lives — keeps producers free of test-driven interface noise
- Accept interfaces, return concrete types — callers get flexibility, you keep options open
- An interface with one implementation is usually premature; wait for the second before extracting
- Avoid framework-style "container" packages — a `main` that wires dependencies explicitly beats hidden service locators

## Errors are values

- Errors are returned, not thrown — every error path is visible in the signature
- Wrap with `%w` to preserve the chain: `fmt.Errorf("loading %s: %w", path, err)`
- Sentinel errors (`var ErrNotFound = errors.New(...)`) for predictable conditions; check with `errors.Is`
- Typed errors with fields when callers need to inspect details; check with `errors.As(&target)`
- Don't wrap when adding no information; don't ignore — handle, log with context, or return

## Concurrency design

- Don't reach for goroutines first — sequential code is easier to read and reason about
- Every goroutine needs an exit story: a context, a closed channel, or a `WaitGroup` — leaks compound silently
- `context.Context` is the first parameter of any function that does I/O, blocks, or starts goroutines; never stored in a struct
- Channels coordinate ownership transfer; mutexes guard short critical sections — pick the simpler one for the job
- `errgroup.Group` for "do N things in parallel, fail if any fails"; `sync.WaitGroup` for fire-and-collect
- Close channels from the sender side only; receivers detect closure via the two-value receive
- Shared mutable state crosses fewer goroutines than you think — copy values, send messages, or use immutable snapshots

## Standard library first

- HTTP: `net/http` with `http.ServeMux` (1.22+ supports path params) — frameworks are rarely necessary
- JSON: `encoding/json` with struct tags; for performance-sensitive paths reach for `json.Decoder` streaming
- Logging: `log/slog` for structured logs — replaces third-party loggers in new code
- `io.Reader` / `io.Writer` are the universal data interfaces — write functions in terms of them, not `[]byte` or `string`
- `context`, `errors`, `slices`, `maps`, `cmp` cover most utility needs

## Generics — sparingly

- Generics are for containers and algorithms (`slices.Sort`, `sync.Pool[T]`), not for "abstracting" business logic
- A non-generic helper that takes `any` plus a type assertion is usually worse than two specific functions — but two specific functions are usually fine
- Type parameters on methods are not allowed; design around it

## Project layout

- `cmd/<name>/main.go` for each binary; one `main` package per binary
- `internal/` for packages not importable outside the module — use it liberally to keep the public API small
- `pkg/` only when publishing a reusable library; private services don't need it
- Module path matches the repo's import path; one module per repo unless there's a strong reason otherwise
- Flat over nested — deep package trees fight Go's import-by-name idiom

## Testing

- Table-driven tests with `t.Run(tc.name, ...)` — the canonical Go pattern
- `t.Cleanup` over `defer` for fixtures; `t.TempDir`, `t.Setenv` auto-clean
- Test the public API of a package; reach into internals only when an invariant can't be observed from outside
- Hand-written fakes beat mock frameworks for clarity; `httptest.Server` for HTTP boundaries
- Always run with `-race` in CI; data races are the most common Go bug
