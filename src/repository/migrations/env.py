import asyncio

import sqlalchemy
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool import NullPool as SQLAlchemyNullPool
from src.models.db import *
from src.repository.base import Base
from src.repository.database import async_db


target_metadata = Base.metadata

config = context.config

DATABASE_URL = async_db.set_async_db_uri
config.set_main_option(name="sqlalchemy.url", value=str(DATABASE_URL))

def include_object(object, name, type_, reflected, compare_to):
    """Filter out tables to exclude from migrations."""
    if type_ == "table":
        return False
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, include_object=include_object)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=SQLAlchemyNullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
