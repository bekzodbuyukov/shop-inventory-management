# Shop Inventory Management System

A FastAPI-based backend for managing shop inventory (catalogs and products).

## Features
- **Catalog Management**: Create, Read, Update, Delete catalogs.
- **Product Management**: CRUD for products, filter by catalog, assign products to catalogs.
- **API Documentation**: Built-in Swagger UI at `/docs`.
- **Database**: PostgreSQL with SQLAlchemy and Alembic for migrations.
- **Testing**: Comprehensive tests with `pytest`.
- **Dockerized**: Ready to run with Docker and Docker Compose.

## Prerequisites
- Python 3.11+
- [Pipenv](https://pipenv.pypa.io/)
- Docker & Docker Compose (optional, for containerized setup)

## Running with Docker (Recommended)

The easiest way to get started is using Docker Compose. This will spin up both the application and a PostgreSQL database.

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`.
The documentation (Swagger UI) can be found at `http://localhost:8000/docs`.

## Running Locally (without Docker)

### 1. Setup Environment
Ensure you have a PostgreSQL instance running and update the environment variables or `.env` file accordingly.

```bash
# Create virtual environment and install dependencies
pipenv install --dev
```

### 2. Run Migrations
```bash
pipenv run alembic upgrade head
```

### 3. Start the Server
```bash
pipenv run uvicorn app.main:app --reload
```

## Running Tests

Tests use an in-memory SQLite database, so no external setup is required.

```bash
PYTHONPATH=. pipenv run pytest
```

## Project Structure
- `app/`: Core application logic.
- `app/api/`: API routers and aggregation.
- `app/core/`: Configuration and database setup.
- `app/models/`: SQLAlchemy database models.
- `app/schemas/`: Pydantic data schemas for request/response.
- `app/services/`: Business logic layer.
- `migrations/`: Alembic database migration scripts.
- `tests/`: Unit and integration tests.
