# Python Version Compatibility

## Recommended Python Version

**Python 3.11 or newer** is recommended for production use.

## Current Compatibility Status

### ✅ Works with Python 3.11 - 3.14
- FastAPI, Uvicorn, Starlette
- SQLAlchemy, SQLModel
- Pydantic
- aiosqlite (SQLite async driver)
- psycopg (v3) (PostgreSQL async driver - Python 3.14 compatible)
- All testing and development dependencies

## Installation Instructions

### Installation

```bash
# Install Python 3.11+
brew install python@3.12  # macOS

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

## Production Deployment

**PostgreSQL Production:** Use Python 3.11+ with psycopg (v3)

```bash
# Install dependencies
pip install -r requirements.txt

# Use async PostgreSQL URL (driver auto-detected)
DATABASE_URL=postgresql://user:password@host:5432/db
```

**SQLite Development:** Works with any Python 3.11+

```bash
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

## Checking Your Python Version

```bash
python --version
python3 --version
python3.12 --version
```

## Database Drivers

**PostgreSQL:**
- Sync operations (migrations): `psycopg2-binary`
- Async operations (API): `psycopg` (v3)
- Both drivers are Python 3.14 compatible

**SQLite:**
- Sync operations: built-in `sqlite3`
- Async operations: `aiosqlite`

