# Architecture

This document describes the current architecture of Media Bot and the design decisions behind it.

The architecture is intentionally kept simple while maintaining clear boundaries between Telegram interaction, application logic, data access, and infrastructure.

## Overview

The current dependency flow is:

```text
Telegram
   │
   ▼
Handlers
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
SQLAlchemy
   │
   ▼
PostgreSQL
```

The main goal is to prevent infrastructure and framework-specific concerns from spreading throughout the application.

Each layer should have a clear responsibility and depend only on abstractions or layers below it where appropriate.

## Project Structure

```text
src/media_bot/
├── bot/
│   └── handlers/
├── config/
├── infrastructure/
├── models/
├── repositories/
└── services/
```

### `bot/`

Contains Telegram-specific code.

Handlers receive Telegram updates and translate them into application-level operations.

Handlers should not contain database queries or substantial business logic.

For example, a handler should coordinate an interaction such as:

```text
Telegram update
      ↓
handler
      ↓
service
      ↓
repository
```

rather than performing database operations directly.

### `services/`

Contains application-level use cases.

Services coordinate operations required to fulfill an application action and should remain independent of Telegram-specific details.

This separation allows application behavior to be tested without requiring a Telegram update or handler.

### `repositories/`

Contains data-access logic.

Repositories encapsulate database queries and provide a clear interface for the application layer.

For example, `UserRepository` is responsible for operations involving persisted users rather than requiring services or handlers to construct SQLAlchemy queries themselves.

This keeps SQLAlchemy-specific data-access details out of higher-level application code.

### `models/`

Contains SQLAlchemy ORM models representing persisted application data.

Models describe the database-backed domain structures and their persistence mapping.

They should not become a place for unrelated application workflows.

### `infrastructure/`

Contains infrastructure concerns such as database connectivity and other external resources.

For example, creation of the SQLAlchemy async engine and session factory belongs here rather than inside handlers or services.

### `config/`

Contains application configuration and environment-based settings.

Configuration is loaded and validated separately from the application components that consume it.

This prevents environment-specific details from being hardcoded throughout the codebase.

## Dependency Direction

Dependencies should generally move toward lower-level infrastructure through well-defined boundaries:

```text
Handlers
   ↓
Services
   ↓
Repositories
   ↓
Database infrastructure
```

A lower-level implementation should not require knowledge of higher-level Telegram behavior.

For example:

- A repository should not import an aiogram handler.
- A service should not depend on a Telegram `Message` object merely to perform its core operation.
- A handler may depend on a service.
- A service may depend on a repository.

This makes individual components easier to test and replace.

## Handlers

Handlers are responsible for Telegram-facing concerns.

Their responsibilities include:

- Receiving Telegram updates
- Extracting relevant input
- Calling the appropriate application operation
- Producing the Telegram response

Handlers should remain thin.

Avoid placing business rules, complex validation, or database queries directly inside handlers when that logic belongs to a service or repository.

## Services

Services represent application behavior rather than transport-specific behavior.

A service should answer questions such as:

- What should happen when a user performs an action?
- Which application operations need to happen together?
- What rules determine the result?

Services should not need to know whether the operation was triggered by Telegram, a test, or another future interface.

This separation becomes increasingly important as the project grows beyond a single Telegram interface.

## Repositories

Repositories provide the application's data-access boundary.

For example:

```python id="1v3o8w"
user = await user_repository.get_by_telegram_id(telegram_id)
```

The service does not need to know how that user is retrieved from PostgreSQL.

The repository owns the SQLAlchemy query:

```python id="w72kgl"
statement = select(User).where(User.telegram_id == telegram_id)
result = await self.session.execute(statement)
return result.scalar_one_or_none()
```

This separation keeps database-specific implementation details localized.

Repositories should focus on persistence operations rather than becoming general-purpose business-logic containers.

## Database Sessions

Database sessions are created through the infrastructure layer.

The application uses SQLAlchemy's asynchronous engine and session factory.

The session factory is responsible for creating `AsyncSession` instances, while repositories receive a session and use it for their database operations.

This keeps connection and engine configuration separate from individual repositories.

## Transactions

Transaction boundaries should be explicit.

Application operations that modify multiple pieces of persistent state should define where the transaction begins and ends rather than allowing individual repository methods to make unrelated transaction decisions.

Repository methods should not commit transactions merely because they perform a write unless the repository's contract explicitly requires that behavior.

Keeping transaction management separate from individual queries makes multi-step operations easier to reason about and test.

## Database Migrations

Alembic is used to manage database schema changes.

The database schema should evolve through migrations rather than through manual changes to shared databases.

The general workflow is:

```text
Model change
    ↓
Generate migration
    ↓
Review migration
    ↓
Run migration locally
    ↓
Run tests
    ↓
Commit migration
```

Autogenerated migrations must always be reviewed manually.

An autogenerated migration is a starting point, not a guarantee that the resulting schema change is correct.

Applied migrations should not be rewritten. If a schema change is required after a migration has already been shared or applied, create a new migration.

## Testing Architecture

The test suite is divided into unit and integration tests.

```text
tests/
├── unit/
└── integration/
```

Unit tests should isolate the behavior being tested from external infrastructure whenever practical.

Integration tests verify behavior involving real infrastructure, particularly PostgreSQL.

The separation is intentional:

```text
Unit tests
    ↓
Application behavior

Integration tests
    ↓
Application + PostgreSQL
```

The integration test suite uses a dedicated test database and must not depend on the development database.

Tests should validate behavior and important edge cases rather than implementation details whenever possible.

## Configuration and Environments

Environment-specific configuration is provided through environment variables.

The application configuration is separated into settings such as:

```text
Bot settings
Database settings
```

Development and test environments use separate configuration files.

The test environment must never accidentally connect to the development database.

Secrets such as bot tokens and database passwords must not be committed to the repository.

Only example configuration belongs in `.env.example`.

## Error Handling

Errors should be handled at the layer that has enough context to make an appropriate decision.

Do not catch exceptions merely to suppress them.

Avoid broad exception handling such as:

```python id="x4p0hx"
try:
    ...
except Exception:
    ...
```

unless there is a specific reason and the exception is handled appropriately.

Infrastructure errors should not automatically become Telegram-specific logic.

Likewise, Telegram presentation concerns should not leak into repositories or lower-level database code.

## Async Code

The application uses asynchronous Python for Telegram and database operations.

Async functions should remain asynchronous throughout the relevant call chain.

Avoid blocking operations inside async code.

When an external library or operation is inherently synchronous, its use should be considered carefully so that it does not block the application's event loop.

Future media downloading and processing components should follow the same principle.

## Adding New Components

Before introducing a new abstraction, consider whether an existing layer already has the appropriate responsibility.

For example, do not introduce a new manager, helper, utility, or pattern simply because it makes one piece of code shorter.

A new component should have:

- A clear responsibility
- A clear boundary
- A reason to exist independently
- Tests appropriate to its behavior

Prefer a small number of well-defined components over many narrowly justified abstractions.

## Future Media Architecture

Media providers, downloaders, storage, and delivery components are planned but are not yet part of the current implementation.

The expected direction is:

```text
Telegram
   ↓
Handlers
   ↓
Services
   ↓
Media Provider
   ↓
Downloader
   ↓
Storage
   ↓
Delivery
   ↓
Telegram
```

This is a planned architectural direction, not a description of currently implemented components.

Future implementations should be introduced incrementally and should preserve the existing separation of concerns.

## Design Principles

The architecture follows several principles:

1. Keep responsibilities separated.
2. Keep handlers thin.
3. Keep database access inside repositories.
4. Keep application behavior inside services.
5. Keep infrastructure details isolated.
6. Prefer explicit dependencies over hidden global state.
7. Prefer simple designs over unnecessary abstractions.
8. Test behavior, including important failure cases.
9. Keep external-framework details from leaking into application logic.
10. Optimize for maintainability rather than merely making the current feature work.
::