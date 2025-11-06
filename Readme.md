# Base Fastapi Backend

A comprehensive FastAPI-based backend application for the Foodvery platform.

## Features

- 🔐 **Authentication & Authorization** - JWT-based authentication with refresh tokens
- 📧 **Email Services** - Automated email notifications
- 📊 **Analytics & Monitoring** - Built-in request logging and error tracking
- 🔗 **URL Shortening** - Custom short URL service
- 📄 **Template System** - Manage website templates
- 🎫 **Coupon System** - Discount and promotional codes
- ☁️ **Cloud Storage** - Integration with DigitalOcean Spaces

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with bcrypt
- **Email**: SMTP integration
- **Cloud Storage**: AWS S3/DigitalOcean Spaces (boto3)
- **Task Queue**: Celery with Redis
- **Testing**: Pytest

## Project Structure

```
foodvery-backend/
├── alembic/              # Database migrations
├── common/               # Shared modules (exceptions, response models, email templates)
├── config/               # Application configuration
├── controllers/          # Request handlers
├── database/            # Database models and configuration
├── middlewares/         # Custom middleware
├── routes/              # API routes
├── SDK/                 # SDK modules for external services
├── services/            # Business logic layer
├── tests/               # Test suite
├── utils/               # Utility functions
├── workers/             # Background workers
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (or SQLite for development)
- Redis (for background tasks)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd foodvery-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
alembic upgrade head
```

### Running the Application

Development mode:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=. --cov-report=html
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## API Documentation

Once the application is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Key environment variables (see `.env` for complete list):

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT signing key
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`: Email configuration
- `DO_SPACES_KEY`, `DO_SPACES_SECRET`: Cloud storage credentials
- `DEBUG`: Enable debug mode

## Development

### Code Style

This project follows PEP 8 guidelines. Use the following tools:

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

### Adding New Endpoints

1. Create a response model in `common/response_models/`
2. Create a controller in `controllers/`
3. Create a service in `services/`
4. Register the route in `routes/`
5. Add tests in `tests/`

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a production database (PostgreSQL recommended)
3. Set up proper secret keys
4. Configure HTTPS/SSL
5. Use a production-grade WSGI server (gunicorn)

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Your License Here]

## Support

For support, email support@foodvery.com or open an issue in the repository.

