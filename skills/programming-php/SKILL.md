---
name: programming-php
title: "PHP Development"
description: "Modern PHP 8.x conventions, strict types, Composer, PHPUnit, PHPStan, and Laravel/Symfony best practices. Auto-activates in PHP projects."
license: Apache-2.0
compatibility: "Requires PHP 8.1+ and Composer."
domains: developer
activate:
  - on: any
    rule: file(composer.json)
  - on: user
    rule: content(php)
---

# PHP Development

## Conventions

- `declare(strict_types=1)` — ALWAYS first statement in every PHP file
- Type hints everywhere — parameters, return types, properties
- Constructor promotion for dependency injection and DTOs
- `match` over `switch` — expression, strict comparison, no fall-through
- Enums (8.1+) — backed enums for database/API values
- `readonly` properties/classes — immutability by default for DTOs
- `===` over `==` — always strict comparison
- No closing `?>` tag in pure PHP files

## Type System

- Native types over PHPDoc: `string`, `int`, `float`, `bool`, `?Type`, `Type|null`
- PHPDoc ONLY for generics: `@param array<string, int>`, `@return Collection<int, User>`
- Union types: `int|string`, intersection types: `Countable&Iterator`

## Error Handling

- Custom exception hierarchy extending `RuntimeException` or `LogicException`
- Named constructors: `EntityNotFoundException::forId('User', $id)`
- Catch specific exceptions, never bare `catch(\Exception)`
- Nullsafe operator: `$user?->getAddress()?->getCountry()`

## Testing (PHPUnit 10+)

- Attributes: `#[Test]`, `#[DataProvider('name')]` — not annotations
- `assertSame` > `assertEquals` — strict by default
- Tests in `tests/Unit/`, `tests/Integration/`

## Static Analysis

- PHPStan level 5+ minimum, level 8-9 for new projects
- PHP CS Fixer or Laravel Pint for formatting

## Laravel Conventions

- Eloquent relationships, scopes, casts
- Form Requests for validation, Policies for authorization
- Jobs/Queues for async, Events/Listeners for decoupling

## Symfony Conventions

- Autowiring by default, attributes for routing: `#[Route('/path')]`
- Doctrine ORM, Twig templates
- Console commands, event subscribers, voters

## Tooling

| Command | Purpose |
|---------|---------|
| `composer install` | Install dependencies |
| `./vendor/bin/phpunit` | Run tests |
| `./vendor/bin/phpstan analyse` | Static analysis |
| `./vendor/bin/php-cs-fixer fix` | Format code |
| `php artisan test` | Laravel test runner |
| `php artisan migrate` | Laravel migrations |
