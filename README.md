# Financial Transactions API

FastAPI REST API for financial accounts and transactions, with JWT authentication, SQLAlchemy persistence, Alembic migrations, and layered architecture.

## Features

- FastAPI endpoints for accounts, transactions, and auth token generation
- JWT token verification middleware
- Layered architecture (`api`, `use_cases`, `domain`, `infrastructure`)
- PostgreSQL + SQLAlchemy async session management
- Alembic migrations
- Test suite organized with mirrored folder strategy
- Dockerized runtime with `uvicorn`
- CI pipeline with `uv` + `pyproject.toml` / `uv.lock`

## Project Structure

```text
.
├── app/
│   ├── api/
│   │   ├── security/
│   │   └── v1/routes/
│   ├── core/config/
│   ├── domain/
│   │   ├── entities/
│   │   ├── enums/
│   │   ├── exceptions/
│   │   └── repositories/
│   ├── infrastructure/
│   │   ├── database.py
│   │   └── models/
│   ├── use_cases/
│   │   ├── account/
│   │   └── transaction/
│   └── main.py
├── tests/
│   ├── api/
│   │   ├── security/
│   │   └── v1/routes/
│   ├── domain/repositories/
│   └── use_cases/
├── alembic/
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python `3.14+`
- PostgreSQL `15+` (or compatible)
- `uv` package manager
- Docker (optional)

## Local Setup

1. Clone repository:

```bash
git clone <repository-url>
cd financial-transations
```

2. Install dependencies from `pyproject.toml` + `uv.lock`:

```bash
uv sync
```

3. Configure environment variables (`.env`), for example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/transactions
SECRET_KEY=your-secret
JWT_ALGORITHM=HS256
```

4. Run migrations:

```bash
uv run alembic upgrade head
```

## Run Application

Development mode:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker

Build:

```bash
docker build -t financial-transations .
```

Run:

```bash
docker run --rm -p 8000:8000 financial-transations
```

## Testing

Run all tests:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=. --cov-report=term-missing
```

Current mirrored test layout includes:

- `tests/use_cases/account/`
- `tests/use_cases/transaction/`
- `tests/domain/repositories/`
- `tests/api/v1/routes/`
- `tests/api/security/`

## CI

GitHub Actions (`.github/workflows/ci.yml`) uses:

- Python `3.14`
- `uv sync --frozen` for dependencies
- `uv run pytest --cov=.` for tests

## Main API Routes

- `GET /api/v1/token`
- `POST /api/v1/accounts`
- `GET /api/v1/accounts/{account_id}`
- `POST /api/v1/transactions`
- `GET /api/v1/transactions/{account_id}/account`
