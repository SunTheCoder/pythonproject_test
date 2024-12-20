from logging.config import fileConfig
import os
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context
from app import db  # Import the SQLAlchemy instance
from app import FileMetadata  # Import the models

# Load environment variables from .env
load_dotenv()

# Retrieve DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Alembic Config object
config = context.config

# Dynamically set the database URL
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for autogenerate support
target_metadata = db.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")  # URL is now set dynamically
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
