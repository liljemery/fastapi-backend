# Test Suite

Comprehensive async test suite covering all layers of the application.

## Test Organization

```
tests/
├── conftest.py          # Shared fixtures and configuration
├── test_auth.py         # Authentication endpoint tests (11 tests)
├── test_health.py       # System endpoint tests (2 tests)
├── test_models.py       # Database model tests (4 tests)
├── test_services.py     # Service layer tests (9 tests)
└── test_utils.py        # Utility function tests (6 tests)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::test_login_success -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run tests matching pattern
pytest -k "test_user" -v
```

## Test Coverage

**35 tests** covering:

### Authentication (11 tests)
- ✅ User registration (success, duplicate, weak password)
- ✅ Login (success, invalid credentials, nonexistent user)
- ✅ Get current user (with/without token)
- ✅ Token refresh (valid/invalid)
- ✅ Logout

### Dashboard (3 tests)
- ✅ Authenticated dashboard access
- ✅ No token rejection
- ✅ Invalid token rejection

### System Health (2 tests)
- ✅ Health check endpoint
- ✅ Root information endpoint

### Database Models (4 tests)
- ✅ User model creation
- ✅ Email uniqueness constraint
- ✅ UUID auto-generation
- ✅ Soft delete functionality

### Services (9 tests)
- ✅ User creation
- ✅ Duplicate user handling
- ✅ User authentication
- ✅ Password verification
- ✅ User lookup by email/UUID
- ✅ Inactive account handling

### Utilities (6 tests)
- ✅ Password hashing
- ✅ Password verification
- ✅ Access token creation
- ✅ Refresh token creation
- ✅ Token decoding
- ✅ Invalid token handling

## Test Patterns

### Async Tests
```python
@pytest.mark.asyncio
async def test_example(client: AsyncClient, async_db: AsyncSession):
    response = await client.get("/endpoint")
    assert response.status_code == 200
```

### Service Layer Tests
```python
@pytest.mark.asyncio
async def test_service(async_db: AsyncSession):
    user = await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    assert user.email == "test@example.com"
```

### Exception Testing
```python
@pytest.mark.asyncio
async def test_exception(async_db: AsyncSession):
    with pytest.raises(UserNotFoundException):
        await AuthService.get_user_by_email(db=async_db, email="fake@example.com")
```

## Fixtures

### `async_db`
Async database session with in-memory SQLite. Automatically creates/drops tables.

### `client`
AsyncClient with ASGI transport for testing FastAPI routes. Dependency overrides configured.

## CI/CD Integration

Tests run automatically on GitHub Actions:
- Python 3.11 and 3.12
- Coverage reports uploaded to Codecov
- Runs on push and pull requests

See `.github/workflows/ci.yml` for details.

