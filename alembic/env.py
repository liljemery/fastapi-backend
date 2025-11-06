import os
import importlib
import pkgutil
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, String # type: ignore
from alembic import context # type: ignore
from sqlmodel import SQLModel # type: ignore
import sqlalchemy as sa
from sqlmodel.sql.sqltypes import AutoString  # type: ignore
from config import settings
# Alembic Config object
config = context.config

# Load database URL from Alembic config
DATABASE_URL = settings.DATABASE_URL
print(DATABASE_URL)
# Ensure database URL is set
if not DATABASE_URL:
    raise ValueError("Database URL is missing. Check alembic.ini and ensure sqlalchemy.url is set.")

# Import all models dynamically
def import_models(package_name: str):
    """Dynamically import all models inside the given package."""
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package_name}.{module_name}")

import_models("database.models")

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for Alembic autogeneration
target_metadata = SQLModel.metadata

# Fix AutoString issue by converting it to sa.String
def render_item(type_, obj, autogen_context):
    """Render AutoString as sa.String in Alembic migrations."""
    if type_ == "type" and isinstance(obj, AutoString):
        return "sa.String()"  # Convert AutoString to sa.String
    return False

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    config.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
