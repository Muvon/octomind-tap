---
name: programming-go
title: "Go Development"
description: "Go conventions, idiomatic patterns, concurrency, standard library, and testing best practices. Auto-activates in Go projects."
license: Apache-2.0
compatibility: "Requires Go toolchain (go 1.21+)."
domains: developer
rules:
  - file(go.mod)
  - content(golang)
---

# Go Development

## Conventions

- Simplicity above all — Go's greatest strength is readability
- Explicit over implicit — no magic, no hidden behavior
- Errors are values — handle them explicitly, every time
- Interfaces are small — prefer 1-2 method interfaces
- Composition over inheritance — embed, don't extend
- Standard library first — reach for stdlib before third-party
- `go vet` + `staticcheck` — all code must pass both
- `gofmt` — non-negotiable, always format

## Code Organization

- Flat package structure — avoid deep nesting
- Package names: short, lowercase, no underscores (`auth`, not `auth_service`)
- `cmd/` for binaries, `internal/` for private packages, `pkg/` for public
- One package per directory — no exceptions
- `main` package only in `cmd/<name>/main.go`

## Error Handling

- Always handle errors — never ignore with `_`
- Wrap errors: `fmt.Errorf("loading config: %w", err)`
- Use `errors.Is()` and `errors.As()` for inspection
- Custom error types for domain errors (implement `error` interface)
- Sentinel errors (`var ErrNotFound = errors.New(...)`) for expected conditions
- Return early on error — avoid deep nesting

## Interfaces

- Define interfaces where they are USED, not where types are defined
- Accept interfaces, return concrete types
- Keep interfaces small: `io.Reader`, `io.Writer` are the gold standard
- Don't create interfaces for single implementations — wait for the second

## Concurrency

- Don't communicate by sharing memory — share memory by communicating
- Goroutines are cheap but not free — always have an exit strategy
- `context.Context` for cancellation and deadlines — first parameter always
- `sync.WaitGroup` for goroutine lifecycle management
- `sync.Mutex` for shared state — keep critical sections small
- Channels for coordination, mutexes for state
- `errgroup` for parallel work with error collection
- Never start a goroutine without knowing how it will stop

## Testing

- Table-driven tests — idiomatic Go pattern
- `t.Run()` for subtests with descriptive names
- `testify/assert` for cleaner assertions
- `httptest` for HTTP handler testing
- Use interfaces to make code testable — inject dependencies
- Benchmark with `testing.B` — use `b.ResetTimer()` after setup
- `go test -race` — always run with race detector

## Standard Library Patterns

- `http.Handler` interface for HTTP — compose with middleware
- `context.Context` — propagate through call chains, never store in structs
- `io.Reader` / `io.Writer` — use for streaming
- `encoding/json` — struct tags: `json:"field_name,omitempty"`
- `log/slog` — structured logging (Go 1.21+)

## Performance

- Preallocate slices: `make([]T, 0, knownCap)`
- Use `sync.Pool` for frequently allocated objects
- `strings.Builder` for string concatenation in loops
- Avoid reflection in hot paths
- Profile with pprof: `go tool pprof`

## Tooling

| Command | Purpose |
|---------|---------|
| `go build ./...` | Compile all packages |
| `go test ./...` | Run all tests |
| `go test -race ./...` | Run with race detector |
| `go vet ./...` | Static analysis |
| `gofmt -w .` | Format all files |
| `go mod tidy` | Clean up dependencies |
| `staticcheck ./...` | Extended static analysis |
| `go tool pprof` | CPU/memory profiling |
