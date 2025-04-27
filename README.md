# FastAPI Template Project

A modern backend application template based on FastAPI, integrating various components and best practices required for enterprise-level application development.

English | [简体中文](README_zh.md)

## Features

- ✅ **FastAPI** - Fast and efficient modern Python API framework
- ✅ **Async SQLAlchemy** - Full asynchronous ORM support
- ✅ **PostgreSQL** - Powerful relational database
- ✅ **Alembic** - Database migration tool
- ✅ **Pydantic V2** - Robust data validation
- ✅ **JWT Authentication** - JWT-based secure authentication
- ✅ **UUID Primary Keys** - Using UUID instead of auto-incrementing IDs
- ✅ **Timezone Handling** - Built-in Sydney timezone support
- ✅ **Celery** - Background task processing
- ✅ **Redis** - High-performance cache and message broker
- ✅ **Docker** - Containerized deployment support
- ✅ **Pytest** - Comprehensive testing support
- ✅ **Poetry** - Modern Python dependency management
- ✅ **Loguru** - User-friendly logging system
- ✅ **Pre-configured Environment Variables** - Environment-controlled configuration system
- ✅ **Auto-init Superuser** - Automatic superuser creation on application startup

## Project Structure

```
.
├── alembic/                     # Database migration configuration
├── app/                         # Application code
│   ├── api/                     # API routes
│   │   ├── deps.py              # Dependencies (auth, etc.)
│   │   └── v1/                  # API v1 version
│   │       ├── api.py           # API route registration
│   │       └── endpoints/       # Endpoint implementations
│   │           ├── health.py    # Health check API
│   │           └── time_demo.py # Timezone demo API
│   ├── core/                    # Core modules
│   │   ├── config.py            # Configuration management
│   │   ├── security.py          # Security utilities
│   │   ├── logging.py           # Logging configuration
│   │   └── init_app.py          # App initialization
│   ├── crud/                    # CRUD operations
│   │   ├── base.py              # Base CRUD class
│   │   └── user.py              # User CRUD operations
│   ├── db/                      # Database setup
│   │   ├── base.py              # Import all models
│   │   ├── base_class.py        # Base model class
│   │   └── session.py           # Session management
│   ├── models/                  # SQLAlchemy models
│   │   └── user.py              # User model
│   ├── schemas/                 # Pydantic models
│   │   └── user.py              # User schema
│   ├── services/                # Service layer
│   ├── utils/                   # Utility functions
│   │   └── time.py              # Timezone utilities
│   ├── worker.py                # Celery configuration
│   └── main.py                  # Application entry
├── tests/                       # Test code
│   ├── conftest.py              # Test configuration
│   └── test_health.py           # Health check tests
├── .env                         # Development environment variables
├── .env.example                 # Environment variables example
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker configuration
├── pyproject.toml               # Poetry dependency management
├── .pre-commit-config.yaml      # Pre-commit hook configuration
├── .gitignore                   # Git ignore configuration
└── README.md                    # Project documentation
```

## Quick Start

### Requirements

- Python 3.9+
- PostgreSQL 13+
- Redis 6+

### Using Docker Compose

The simplest way to start is using Docker Compose:

1. Clone the project

```bash
git clone https://github.com/linivek/Fastapi_template.git
cd Fastapi_template
```

2. Configure environment variables

```bash
cp .env.example .env
# Edit .env file to suit your environment
```

3. Start all services

```bash
docker-compose up -d
```

4. Access API documentation

```
http://localhost:8000/docs
```

### Local Development Environment

1. Clone the project

```bash
git clone https://github.com/linivek/Fastapi_template.git
cd Fastapi_template
```

2. Install dependencies

```bash
# Install Poetry
pip install poetry

# Install dependencies
poetry install
```

3. Configure environment variables

```bash
cp .env.example .env
# Edit .env file to suit your environment
```

4. Run database migrations

```bash
poetry run alembic upgrade head
```

5. Start the application

```bash
poetry run uvicorn app.main:app --reload
```

## Core Features

### Environment Variables Configuration

This template uses `.env` file for configuration, including:

- **Project Settings** - Project name, API prefix
- **Server Settings** - Host address, port
- **Security Settings** - JWT secret key, algorithm, token expiration time
- **Database Settings** - PostgreSQL connection info
- **Redis Settings** - Redis server info
- **Celery Configuration** - Background task settings
- **Superuser Configuration** - Initial superuser info
- **Timezone Configuration** - Default to Australia/Sydney timezone

Refer to `.env.example` for detailed configuration.

### Database Migrations

Use Alembic for database migrations:

```bash
# Create migration
poetry run alembic revision --autogenerate -m "migration description"

# Apply migration
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1
```

### UUID Primary Keys

This template uses UUID as primary keys for user tables, offering advantages over auto-incrementing IDs:

- Global uniqueness, avoiding ID conflicts
- Enhanced security, harder to guess
- Suitable for distributed systems

Implemented in `app/models/user.py`, using PostgreSQL native UUID type.

### Timezone Handling

The template provides complete timezone support, defaulting to Australia/Sydney timezone:

- Stores UTC time in database (with timezone info)
- Automatically converts to Sydney timezone in API responses
- Provides timezone conversion utilities in `app/utils/time.py`
- Includes time conversion demo API `/api/v1/time`

### JWT Authentication

Built-in complete JWT authentication support:

- Use `/api/v1/auth/login` endpoint to obtain token
- Support username or email login
- Configurable token expiration time
- Includes token refresh mechanism

### Celery Background Tasks

Integrates Celery for background task processing:

- Uses Redis as message broker
- Supports task status tracking
- Includes example task in `app/worker.py`
- Configurable task timeout

### Testing Support

Uses Pytest for testing:

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_health.py

# Show test coverage report
poetry run pytest --cov=app
```

### Code Quality Tools

Integrates multiple code quality tools:

- **Black** - Code formatting
- **Flake8** - Code style checking
- **isort** - Import statement sorting
- **pre-commit** - Git pre-commit checks

Run code quality checks:

```bash
# Install pre-commit hooks
pre-commit install

# Manually run all checks
pre-commit run --all-files
```

## Contributing

Contributions are welcome! Please ensure before submitting a Pull Request:

1. Update test cases
2. Update documentation
3. Follow code style guidelines
4. Add necessary comments

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details