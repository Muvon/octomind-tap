---
name: programming-php
title: "PHP Development"
description: "Modern PHP 8.x architecture, strict types, framework patterns (Laravel/Symfony), and domain modeling. Auto-activates in PHP projects."
license: Apache-2.0
compatibility: "Requires PHP 8.2+ and Composer."
domains: developer
rules:
  - file(composer.json)
  - content(php)
---

## Mental model

Modern PHP is a strictly-typed, object-oriented language with mature frameworks (Laravel, Symfony) covering routing, persistence, queues, and templating. The maintenance trap is writing PHP as if it were still 5.x: untyped arrays as data, controllers full of business logic, Eloquent/Doctrine calls scattered across the app, and global state via facades and singletons. Build a typed domain layer, keep the framework at the edges.

## Type-driven design

- `declare(strict_types=1);` at the top of every file — non-negotiable
- Native types everywhere: parameters, return types, properties — `mixed` only at boundaries with foreign data
- Readonly properties / readonly classes (8.2+) for DTOs and value objects — immutability is the default
- Constructor property promotion for DTOs and services — less boilerplate, clearer intent
- Backed enums for finite sets (status, role, currency) — never string constants
- Union and intersection types when the type system supports the real shape

## Architecture

- Separate domain, application, and infrastructure layers — controllers and Eloquent models are infrastructure, not the domain
- Domain in framework-free PHP: entities, value objects, domain services, repository interfaces
- Application layer: command/query handlers or service classes orchestrating domain operations
- Infrastructure: Eloquent/Doctrine implementations of repository interfaces, HTTP/queue adapters
- Dependency direction inward — the domain knows nothing about Laravel or Symfony

## Error handling

- Custom exception hierarchy per bounded context, rooted at one base extending `RuntimeException` or `DomainException`
- Named constructors for clarity: `UserNotFound::withId($id)` over `new UserNotFound("user 42 not found")`
- Catch specific exceptions; never `catch (\Exception)` outside the outermost handler
- Don't use exceptions for predictable control flow — return a Result-shaped value or `null` for "not found"

## Laravel conventions

- Form Requests for input validation and authorization; controllers stay thin
- Policies for authorization rules; never inline `if` checks scattered through controllers
- Eloquent models hold persistence and trivial accessors — business rules belong in services or domain objects
- Service classes (`app/Services/` or a domain-oriented namespace) for orchestration
- Jobs for async work; Events + Listeners for decoupling side effects
- Migrations describe schema evolution; seeders for reference data; factories for test fixtures
- Avoid Facades in business logic — inject dependencies via the container

## Symfony conventions

- Autowiring with constructor injection; attributes (`#[Route]`, `#[AsCommand]`, `#[AsEventListener]`) over YAML
- Doctrine entities with repository services; queries via DQL or the query builder, encapsulated in repositories
- Symfony Messenger for command/query buses and async workers
- Form component for complex inputs; plain DTOs + Validator for JSON APIs
- Voters for authorization; never inline `is_granted` chains
- Twig for server-rendered HTML; component libraries (Symfony UX) for richer UI

## Data and persistence

- Repository interfaces in the domain, implementations in infrastructure — keeps the domain testable without a database
- Transactions wrap multi-step writes; use the framework's transaction helper or a UoW pattern
- Migrations are immutable in production; new changes are new migrations
- Avoid N+1 queries — eager-load relationships explicitly (`with(...)` in Eloquent, `fetchJoin` in Doctrine)
- Pagination on every list endpoint that can grow unbounded

## Testing

- PHPUnit (10+) with attributes (`#[Test]`, `#[DataProvider]`) for unit and integration tests
- Pest for projects that want a more expressive DSL
- Unit tests on the domain layer — no database, no HTTP, no framework
- Integration tests use the framework's testing kernel with a test database
- `assertSame` over `assertEquals` — strict comparison catches type-juggling bugs
- Fakes over mocks for collaborators you own; use mocking libraries sparingly

## API and HTTP

- JSON APIs return resource representations, not Eloquent models directly — use API Resources (Laravel) or Serializer (Symfony)
- Validate input at the controller boundary; the domain trusts its inputs
- HTTP status codes match semantics: 422 for validation, 404 for missing, 409 for conflict, 5xx only for genuine server errors
- Idempotency keys for unsafe operations exposed publicly

## Project layout

- PSR-4 autoload from `src/` (libraries) or `app/` (Laravel apps)
- Group by feature/bounded context, not by technical layer — `src/Billing/{Domain,Application,Infrastructure}` beats `src/{Models,Controllers,Services}`
- Composer scripts (`composer test`, `composer analyse`) for the common dev workflows
- Configuration in environment variables, loaded via the framework's config layer; secrets never in code
