---
name: programming-typescript
title: "TypeScript Development"
description: "TypeScript conventions, strict type safety, modern JS/TS patterns, and npm ecosystem best practices. Auto-activates in TypeScript projects."
license: Apache-2.0
compatibility: "Requires Node.js and npm/pnpm/yarn."
capabilities: programming-nodejs
domains: developer
rules:
  - file(tsconfig.json)
  - content(typescript)
---

# TypeScript Development

## Conventions

- Type safety first — leverage TypeScript's type system fully
- Strict mode — always `strict: true` in tsconfig.json
- Prefer interfaces — for object shapes, use `interface` over `type`
- Use const assertions — for literal types and readonly arrays
- Avoid `any` — use `unknown` when type is truly unknown
- Minimize non-null assertions (`!`) — prefer proper null checks
- Generic constraints — constrain generics with `extends`
- Utility types — use `Partial`, `Required`, `Pick`, `Omit`, `Record`

## Type Definitions

- Prefer `interface` for object shapes (extendable, better error messages)
- Use `type` for unions, intersections, mapped types
- Declare global types in `.d.ts` files
- Use `typeof` for deriving types from values
- Use `keyof` for key extraction
- `satisfies` operator for type checking without widening
- Discriminated unions for variant types with `kind`/`type` field

## Error Handling

- Use Result/Either pattern for expected errors
- Throw for unexpected/programming errors only
- Type errors with custom error classes extending `Error`
- Use `unknown` in catch blocks (TS 4.4+)
- Never catch and ignore — at minimum log

## Async Patterns

- Prefer `async`/`await` over raw promises
- Use `Promise<T>` for async return types
- Handle promise rejections explicitly
- Use `AbortController` for cancellable operations
- `Promise.all()` for parallel, `Promise.allSettled()` when partial results needed

## Project Structure

- `src/` for source code, `dist/` or `build/` for compiled output
- `tests/` or `__tests__/` for test files
- `types/` or `@types/` for type definitions
- Use path aliases in tsconfig for clean imports
- Barrel exports (`index.ts`) for public API only

## Testing

- Vitest or Jest for unit tests
- Use `describe`/`it` pattern
- Mock with `vi.mock` or `jest.mock`
- Type test files with `.test.ts` or `.spec.ts`
- MSW for mocking HTTP at network level

## Performance

- Use `const` where possible — enables better inference
- Prefer `readonly` for immutable data
- Use `Record<string, T>` for typed objects
- Avoid type assertions — let inference work
- Tree-shaking: use named exports, avoid side effects
