# Financial Transactions API

A FastAPI-based REST API for managing financial transactions with authentication, domain-driven design, and PostgreSQL persistence.

## Features

- **RESTful API** built with FastAPI
- **Authentication** with JWT token-based security
- **Domain-Driven Design** with clear separation of concerns
- **Transaction Management** with comprehensive reporting
- **Database Migrations** using Alembic
- **PostgreSQL** database with SQLAlchemy ORM
- **Docker Support** for containerized deployment
- **Comprehensive Testing** with pytest and code coverage
- **Structured Logging** for debugging and monitoring

## Project Structure

```
.
├── application/              # Application layer (use cases, DTOs)
│   ├── config/              # Configuration (logging)
│   ├── dtos/                # Data Transfer Objects
│   └── use_cases/           # Business logic
├── auth_token/              # Authentication token generation
├── domain/                  # Domain layer (entities, exceptions)
│   ├── entities/            # Core domain entities
│   ├── enums/               # Domain enumerations
│   ├── exceptions/          # Custom exceptions
│   └── repositories/        # Repository interfaces
├── infrastructure/          # Infrastructure layer (database, repositories)
│   ├── database.py          # Database configuration
│   ├── models/              # SQLAlchemy models
│   └── repositories/        # Repository implementations
├── interfaces/              # Interfaces layer (API routes)
│   └── api/
│       ├── routes/          # API endpoints
│       └── security/        # Security utilities
├── migrations/              # Alembic database migrations
├── tests/                   # Test suite
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
└── docker-compose.yml       # Docker Compose for local development
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd financial-transations
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file (or set directly)
   DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/transactions
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://0.0.0.0:8000`

### Using Docker Compose

```bash
docker-compose up --build
```

## API Endpoints

### Authentication

- **GET** `/api/v1/token` - Generate access token
  ```bash
  curl http://localhost:8000/api/v1/token
  ```

### Transactions

- **POST** `/api/v1/transactions` - Create a new transaction
  - Requires valid JWT token in Authorization header
  - Request body: CreateTransactionDTO

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg2://postgres:postgres@localhost:5432/transactions` |

## Testing

Run the test suite with coverage:

```bash
pytest --cov=. --cov-report=html
```

Test files are located in the `tests/` directory and cover:
- DTOs validation
- Use case execution
- Transaction creation
- Report generation
- Factory pattern implementation

View coverage report at `htmlcov/index.html`

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

## Architecture

This project follows **Domain-Driven Design (DDD)** principles:

- **Domain Layer** - Core business logic and entities
- **Application Layer** - Use cases and business workflows
- **Infrastructure Layer** - Data persistence and external services
- **Interfaces Layer** - API endpoints and external communication

## Logging

Logging is configured in `application/config/logging_config.py`. Logs are output to console with detailed information about application flow and errors.

## License

[Add your license information here]

## Support

For issues or questions, please open an issue in the repository.
