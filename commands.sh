#!/bin/bash
# =============================================================================
# FastAPI Backend Template - Development Commands
# =============================================================================
# Common commands for development, testing, and deployment
# Usage: Copy and paste commands as needed (this is a reference, not a script)
# =============================================================================

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1
# Windows CMD:
# venv\Scripts\activate.bat

# Deactivate virtual environment
deactivate

# Install dependencies
pip install -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Update requirements.txt (after installing new packages)
pip freeze > requirements.txt

# =============================================================================
# DEVELOPMENT SERVER
# =============================================================================

# Run development server (with auto-reload)
python main.py

# Run with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run with specific log level
uvicorn main:app --reload --log-level debug

# Run with multiple workers (production-like)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# =============================================================================
# DATABASE MIGRATIONS
# =============================================================================

# Create new migration (auto-generate from models)
alembic revision --autogenerate -m "description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Show current migration version
alembic current

# Show migration history
alembic history

# Create and apply migration (one-liner)
alembic revision --autogenerate -m "updates" && alembic upgrade head

# =============================================================================
# TESTING
# =============================================================================

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with logs visible
pytest -v --log-cli-level=INFO

# Run tests with coverage report
pytest --cov=. --cov-report=html

# Run tests with coverage in terminal
pytest --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py -v

# Run tests matching pattern
pytest -k "test_user" -v

# Run tests with specific markers
pytest -m "unit" -v

# =============================================================================
# TYPE CHECKING & LINTING
# =============================================================================

# Run type checking with MyPy
mypy .

# Run MyPy with specific configuration
mypy . --config-file mypy.ini

# Clear MyPy cache and rerun
rm -rf .mypy_cache/ && mypy .

# Run MyPy and tests together
rm -rf .mypy_cache/ && mypy . && pytest tests/ -v

# =============================================================================
# CODE QUALITY
# =============================================================================

# Format code with Black (if installed)
# black .

# Sort imports with isort (if installed)
# isort .

# Lint with ruff (if installed)
# ruff check .

# =============================================================================
# DOCKER COMMANDS
# =============================================================================

# Build and start all services
docker compose up --build -d

# Start services (without rebuild)
docker compose up -d

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs (follow mode)
docker compose logs -f

# View logs for specific service
docker compose logs -f api

# Restart specific service
docker compose restart api

# Execute command in running container
docker compose exec api /bin/bash

# Execute Python shell in container
docker compose exec api python

# =============================================================================
# DATABASE (Docker)
# =============================================================================

# PostgreSQL (recommended for production)
docker run -d \
  --name postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 \
  postgres:15-alpine

# SQLite (development only - already included)
# No Docker needed, uses local file: test.db

# Access PostgreSQL CLI
docker exec -it postgres psql -U admin -d fastapi_db

# Stop and remove database container
docker stop postgres && docker rm postgres

# =============================================================================
# PRODUCTION DEPLOYMENT
# =============================================================================

# Run with Gunicorn + Uvicorn workers (production)
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info

# Check environment variables
printenv | grep -E "DATABASE_URL|SECRET_KEY|ENVIRONMENT"

# Validate configuration
python -c "from config import settings; print(f'Environment: {settings.ENVIRONMENT}')"

# =============================================================================
# UTILITY COMMANDS
# =============================================================================

# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Check Python version
python --version

# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Create .env from example
cp .env.example .env

# Verify async database setup
python -c "from database import async_engine; print('Async engine configured')"

# =============================================================================
# CLEANUP
# =============================================================================

# Remove Python cache files
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Remove MyPy cache
rm -rf .mypy_cache/

# Remove pytest cache
rm -rf .pytest_cache/

# Remove coverage reports
rm -rf htmlcov/ .coverage

# Full cleanup (cache + test artifacts)
find . -type d -name __pycache__ -exec rm -r {} + && \
  rm -rf .mypy_cache/ .pytest_cache/ htmlcov/ .coverage

# =============================================================================
# TROUBLESHOOTING
# =============================================================================

# Check if port 8000 is in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)

# Check database connectivity
python -c "from database import engine; print('Database connected')"

# Verify imports
python -c "from main import app; print('App imported successfully')"

# =============================================================================
# NOTES
# =============================================================================
# - Always activate virtual environment before running commands
# - Set ENVIRONMENT=production for production deployments
# - Never commit .env file or test.db to version control
# - Run migrations before deploying new code
# - Use PostgreSQL in production (not SQLite)
# - See ARCHITECTURE.md for detailed documentation
# =============================================================================
