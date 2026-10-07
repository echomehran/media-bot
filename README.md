# Media Bot

A Telegram bot for downloading and delivering media from supported sources.

The project is built as a maintainable backend application with a focus on clean architecture, testing, database design, and professional development practices.

## Features

- Telegram bot interface
- User management and persistence
- PostgreSQL database
- Asynchronous application and database operations
- Repository-based data access
- Database migrations with Alembic
- Automated testing with pytest
- Continuous Integration with GitHub Actions

Media provider and downloader support will be developed incrementally.

## Architecture

The project separates Telegram interaction, application logic, data access, and infrastructure concerns.

```text
Telegram
   │
   ▼
Handlers
   │
   ▼
Application / Services
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

The repository layer isolates database access from the application layer, while services contain application-level use cases.

Additional components such as media providers, downloaders, storage, and delivery will be introduced as the media workflow evolves.

For a more detailed explanation of the current architecture and design decisions, see [`docs/architecture.md`](docs/architecture.md).

## Tech Stack

- Python
- aiogram
- SQLAlchemy
- PostgreSQL
- Alembic
- pytest
- Ruff
- uv
- GitHub Actions

## Project Structure

```text
media-bot/
├── src/
│   └── media_bot/
│       ├── bot/
│       ├── config/
│       ├── infrastructure/
│       ├── models/
│       ├── repositories/
│       └── services/
├── tests/
│   ├── unit/
│   └── integration/
├── migrations/
├── docs/
├── pyproject.toml
└── README.md
```

## Development

The project uses `uv` for Python environment and dependency management.

Install dependencies:

```bash
uv sync --dev
```

Create local environment configuration:

```bash
cp .env.example .env
```

Set the required environment variables in `.env`:

```env
BOT_TOKEN=
DATABASE_URL=
```

Run database migrations:

```bash
uv run alembic upgrade head
```

Run the test suite:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

## Database

PostgreSQL is used as the application's primary database.

Database schema changes are managed through Alembic migrations.

To apply all pending migrations:

```bash
uv run alembic upgrade head
```

Integration tests use a dedicated test database and must not depend on the development database.

## Testing

Tests are divided into two main categories:

- `tests/unit/` for isolated application behavior
- `tests/integration/` for behavior involving external infrastructure such as PostgreSQL

The test suite is also executed automatically by GitHub Actions for pushes and pull requests.

## Contributing

Contributions are welcome.

Before making changes, please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for the project's development workflow, commit conventions, testing requirements, and pull request process.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.