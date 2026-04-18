---
name: programming-cpp
title: "C++ Development"
description: "Modern C++20/23 conventions, RAII, smart pointers, CMake, sanitizers, and safe systems programming best practices. Auto-activates in C++ projects."
license: Apache-2.0
compatibility: "Requires C++ compiler (clang/gcc) and CMake."
domains: developer
---

# C++ Development

## Conventions

- Modern C++ — default to C++20, C++23 features when project opts in
- RAII everywhere — all resources managed by constructor/destructor
- Smart pointers — `std::unique_ptr` by default, `std::shared_ptr` only for shared ownership
- NEVER raw `new`/`delete` — use `std::make_unique`, `std::make_shared`, containers
- `const` correctness — `const` on member functions, parameters, locals wherever possible
- Rule of 0 — prefer no custom destructor/copy/move; if you customize one, implement all 5
- `[[nodiscard]]` on functions where ignoring return is likely a bug
- `override` on ALL virtual overrides

## Memory Safety

- `std::unique_ptr` for exclusive ownership, `std::shared_ptr` for shared
- `std::string_view` / `std::span` for non-owning references — watch lifetime
- Never return references or `string_view` to locals or temporaries
- Always initialize variables — C++ does NOT zero-initialize locals
- `noexcept` on move constructors, move assignments, and destructors

## Modern Features

- Structured bindings: `auto [key, value] = pair;`
- `std::optional` for nullable, `std::variant` for sum types
- `std::expected` (C++23) for error handling without exceptions
- Concepts over SFINAE: `template<std::integral T>`
- Ranges: `std::ranges::sort(vec)`
- `std::format` / `std::print` over iostream
- `if constexpr` for compile-time branching
- `std::jthread` over `std::thread` (auto-joining)

## Error Handling

- Exceptions for truly exceptional cases
- `std::expected` (C++23) or Result-type for expected errors
- Error codes at API boundaries where exceptions can't cross
- RAII ensures cleanup regardless of error path

## Build System (CMake)

- Modern target-based: `target_link_libraries`, `target_include_directories`
- No global `include_directories()` or `link_libraries()`
- FetchContent or vcpkg/conan for dependencies
- `CMAKE_EXPORT_COMPILE_COMMANDS=ON` for tooling
- Minimum CMake 3.21+

## Testing & Sanitizers

- Google Test or Catch2 — both integrate with ctest
- Test with sanitizers enabled (ASan + UBSan)
- ASan: `-fsanitize=address` — buffer overflow, use-after-free, leaks
- UBSan: `-fsanitize=undefined` — signed overflow, null deref
- TSan: `-fsanitize=thread` — data races
- Compiler warnings: `-Wall -Wextra -Wpedantic -Werror`

## Common Pitfalls

- Dangling references: returning `string_view`/`const&` to temporaries
- Use-after-move: accessing objects after `std::move`
- Signed/unsigned mixing: `int` vs `size_t` comparison bugs
- Missing `virtual` destructor on polymorphic base classes
- Object slicing: passing derived by value to base parameter

## Tooling

| Command | Purpose |
|---------|---------|
| `cmake -B build && cmake --build build` | Configure and build |
| `ctest --test-dir build` | Run tests |
| `clang-tidy -p build src/*.cpp` | Lint |
| `clang-format -i src/*.cpp` | Format |
