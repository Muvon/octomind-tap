---
name: programming-cpp
title: "C++ Development"
description: "Modern C++ architecture, RAII, value semantics, and library choices that survive a decade. Auto-activates in C++ projects."
license: Apache-2.0
compatibility: "Requires the project's C++ compiler, standard library, and build system."
domains: developer
rules:
  - file(CMakeLists.txt)
  - file(meson.build)
  - file(conanfile.txt)
  - file(conanfile.py)
  - file(vcpkg.json)
  - content(c++)
  - content(cpp)
---

## Overview

Write modern C++ with value semantics, deterministic resource cleanup, and explicit lifetime contracts. Research baseline: C++23 is the published ISO standard; C++26 remains in progress, checked 2026-09-05. Read build presets, compiler versions, selected language standard, standard-library implementation, and CI targets first. A compiler accepting `-std=c++23` does not prove every C++23 library facility is available. Recheck vendor support tables when adopting features.

## Mental model

Every resource has an owner; every view has a lifetime. Prefer values and standard containers. RAII (resource acquisition is initialization) makes cleanup follow scope exit, including exceptions, but does not automatically prevent dangling references or unsynchronized shared mutation.

## Modern features, gated by support

| Standard | Useful facilities |
|----------|-------------------|
| C++20 | Concepts, ranges, `std::span`, `std::format`, `std::jthread`/stop tokens, `consteval`, `constinit`. |
| C++23 | `std::expected`, `std::print`, `std::ranges::to`, explicit object parameters, `std::mdspan`. |

Use concepts to express template requirements and ranges when the resulting pipeline is clearer than a loop. `std::format` is C++20; `std::print` is C++23. Neither guarantees a performance win for your workload. Modules and newer library features need compiler, library, and build-system support; don't introduce a migration or compatibility wrapper merely to use newer syntax. Treat C++26 reflection, contracts, and execution facilities as evolving until the project's implementation and intended standard explicitly support them.

## Ownership and lifetime

- Let RAII members implement cleanup and copying/moving where they match the type's semantics: the rule of zero. For direct resource owners, define or delete the relevant special members deliberately.
- Use `unique_ptr` for exclusive dynamic ownership; use `shared_ptr` only for shared lifetime, with `weak_ptr` where needed to avoid ownership cycles. Shared ownership does not synchronize the pointed-to object.
- Raw pointers, references, `string_view`, and `span` ordinarily borrow. Don't retain or return them beyond their backing storage's lifetime. Container reallocation and mutation can invalidate views and iterators; lazy ranges may retain references to predicates and source storage.
- Pass cheap values by value and expensive read-only inputs by `const&`. Transfer ownership explicitly. Return values naturally; `return std::move(local)` can prevent named return value optimization.
- Standard-library moved-from objects are generally valid but unspecified unless documented otherwise. Check operation preconditions before reuse; custom types must define their own valid moved-from behavior.
- A base intended for deletion through a base pointer needs a public virtual destructor; a protected nonvirtual destructor can prohibit that operation. Avoid object slicing when passing polymorphic values.

## Types, errors, and numeric correctness

- Use `optional` for expected absence, `variant` for closed alternatives, and `expected<T, E>` for explicit recoverable failure where compatible with the project's error model. Don't replace established exceptions globally.
- An `expected` must be checked before unchecked value access. Preserve meaningful errors; don't convert failed parsing, I/O, or configuration into a successful empty object or zero.
- Mark results `[[nodiscard]]` when discarding them usually violates the contract. Keep destructors nonthrowing; use an explicit operation when callers need to observe finalization errors.
- Initialize values, validate narrowing conversions, and check arithmetic that can overflow. Signed integer overflow is undefined behavior. Parse complete input: successful prefix parsing must not silently accept trailing junk.
- Keep casts and raw-memory manipulation at explicit interoperability boundaries. Document alignment, lifetime, aliasing, and ownership assumptions; don't bypass the type system to silence a diagnostic.

## Concurrency and build boundaries

- Prefer scoped task ownership. A `jthread` requests stop and joins when destroyed; stopping is cooperative, so blocking operations need a way to wake. Captured references must remain alive until work finishes.
- Protect compound shared invariants with a mutex. Atomic variables alone don't make a multi-step algorithm safe, and `std::atomic<T>` is not guaranteed lock-free. Weaker memory ordering needs a correctness argument, not just a benchmark.
- `const&` does not prove thread safety: another alias may mutate the same object. Establish lifetime and synchronization before sharing access.
- In CMake, attach features, include paths, and dependencies to targets. Use `PRIVATE`, `PUBLIC`, and `INTERFACE` to express actual consumer requirements. Preserve the existing dependency manager and reproducible version policy.

## Example

C++23: preserve failure as an explicit alternative instead of substituting a default.

```cpp
#include <expected>

enum class WorkerError { non_positive };

[[nodiscard]] std::expected<unsigned, WorkerError> worker_count(int value) {
    if (value <= 0) {
        return std::unexpected(WorkerError::non_positive);
    }
    return static_cast<unsigned>(value);
}
```

## Checklist

- [ ] Features work across the project's compiler, library, standard, and target matrix.
- [ ] Resources, borrowed lifetimes, moves, error paths, and synchronization have explicit contracts.
- [ ] No silent defaults, unsafe narrowing, or unnecessary ownership/architecture expansion.
- [ ] When authorized, use project formatting, warnings, focused tests, and applicable sanitizers. Check invalid input and lifetime boundaries; report checks skipped.

## References

- [Published standard](https://isocpp.org/std/the-standard), [GCC support](https://gcc.gnu.org/projects/cxx-status.html), and [Clang support](https://clang.llvm.org/cxx_status.html).
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
- Working-draft contracts: [expected](https://eel.is/c++draft/expected), [moved-from library objects](https://eel.is/c++draft/lib.types.movedfrom), [format](https://eel.is/c++draft/format), and [jthread](https://eel.is/c++draft/thread.jthread.class). Check the selected standard before using draft additions.
- [CMake target model](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html).
