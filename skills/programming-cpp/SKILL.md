---
name: programming-cpp
title: "C++ Development"
description: "Modern C++ architecture, RAII, value semantics, and library choices that survive a decade. Auto-activates in C++ projects."
license: Apache-2.0
compatibility: "Requires a C++20-capable compiler and a build system (CMake, Meson)."
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

## Mental model

Modern C++ is a value-semantic language with optional escape hatches. The maintainable subset is small: RAII for resources, values by default, references for non-owning views, smart pointers when ownership is dynamic, and `std::` containers/algorithms over hand-rolled equivalents. Most C++ misery comes from importing patterns from C (manual new/delete), Java (everything heap-allocated and polymorphic), or pre-C++11 codebases.

## Ownership and resource management

- RAII handles every resource: memory, files, sockets, locks, GPU handles — wrap raw resources in a type whose destructor releases them
- `std::unique_ptr<T>` is the default for dynamic ownership; `std::shared_ptr<T>` only when ownership is genuinely shared (and document why)
- `std::make_unique` / `std::make_shared` — raw `new` is a code smell outside placement-new contexts
- Rule of zero by default: if all members are RAII types, the compiler-generated special members are correct
- Rule of five only when managing a resource directly; mark move operations `noexcept` or containers fall back to copies

## Value semantics over polymorphism

- Pass small types by value, large types by `const&`, sink parameters by value (then move into place)
- Return by value — RVO and move semantics make it cheap; out-parameters are a 1990s habit
- Reach for inheritance only when runtime polymorphism is actually needed (plugin boundaries, framework hooks); virtual functions are not the default
- `std::variant` + `std::visit` for closed sum types — far easier to reason about than a class hierarchy
- `std::optional<T>` for "maybe a value"; `std::expected<T, E>` (C++23) for "value or error"

## Lifetime hazards

- `std::string_view` and `std::span<T>` are non-owning — never return them referring to locals or temporaries
- A reference or pointer outlives the referent silently; prefer values in struct members unless the borrow is structurally clear
- A moved-from object is valid but unspecified — assign or destroy before reading
- Polymorphic base classes need a virtual destructor; without one, `delete base_ptr` is undefined behavior
- Object slicing on by-value polymorphic parameters silently drops derived state — take `const Base&`

## Modern features worth standardizing on

- Concepts (`template<std::integral T>` or `requires`) — replace SFINAE, dramatically improve diagnostics
- `std::ranges` and views for composable algorithms over containers
- `if constexpr`, `consteval`, `constinit` for compile-time computation and enforcement
- `std::format` / `std::print` (C++23) — typesafe, much faster than iostreams
- `std::jthread` with `std::stop_token` for cooperative cancellation; `std::thread` is legacy
- `[[nodiscard]]` on factories and error-returning functions

## Concurrency

- Prefer a higher-level model (task system, executors, message passing) over raw threads and locks
- A `std::mutex` should protect a tiny critical section — long-held locks are a design failure
- `std::atomic<T>` for lock-free counters and flags; sequential consistency unless profiling proves a weaker order safe
- Pass `const&` data across thread boundaries; mutable shared state needs synchronization or single-owner discipline
- Async I/O via a library (Asio, libuv, executors proposal) — don't hand-roll event loops

## Project layout and build

- CMake with modern target-based commands (`target_link_libraries`, `target_include_directories`); avoid global `include_directories` and `link_libraries`
- `PUBLIC` / `PRIVATE` / `INTERFACE` propagation matters — use them deliberately so consumers inherit only what they need
- Headers under `include/<project>/...`, sources under `src/`; one logical component per directory
- Dependencies via vcpkg, Conan, or `FetchContent` — not git submodules
- Compile with high warnings on (`-Wall -Wextra -Wpedantic`, `/W4`) and treat warnings as errors in CI

## Ecosystem defaults

- Containers and algorithms: `std::` first, Abseil/Folly for what's missing
- Logging: `spdlog`
- Testing: GoogleTest or Catch2
- HTTP server/client: cpp-httplib for simple cases, Beast/Asio for scale
- JSON: `nlohmann/json` for ergonomics, `simdjson` for performance
- CLI parsing: CLI11 or `argparse`
