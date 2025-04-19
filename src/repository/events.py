import asyncio

import fastapi
import loguru
import sqlalchemy
from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_connection
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from sqlalchemy.pool.base import _ConnectionRecord

from src.repository.database import async_db
from src.repository.table import Base


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="connect")
def inspect_db_server_on_connection(
    db_api_connection: AsyncAdapt_asyncpg_connection,
    connection_record: _ConnectionRecord,
) -> None:
    loguru.logger.info(f"New DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Connection Record ---\n {connection_record}")


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="close")
def inspect_db_server_on_close(
    db_api_connection: AsyncAdapt_asyncpg_connection,
    connection_record: _ConnectionRecord,
) -> None:
    loguru.logger.info(f"Closing DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Closed Connection Record ---\n {connection_record}")


# Drop all Tables and Creates All Table Again
async def initialize_db_tables(connection: AsyncConnection) -> None:
    loguru.logger.info("Database Table Creation --- Initializing . . .")

    await connection.run_sync(Base.metadata.create_all)
    loguru.logger.info("Database Table Creation --- Successfully Initialized!")


async def initialize_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Establishing . . .")

    backend_app.state.db = async_db

    async with backend_app.state.db.async_engine.begin() as connection:
        await initialize_db_tables(connection=connection)

    loguru.logger.info("Database Connection --- Successfully Established!")


async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection - Disposing . . .")

    try:
        pool_status = async_db.async_engine.pool.status()
        loguru.logger.info(f"Pool Status Before Closing: {pool_status}")

        await backend_app.state.db.async_engine.dispose()

        pool_status_after = async_db.async_engine.pool.status()
        loguru.logger.info(f"Pool Status After Closing: {pool_status_after}")
        loguru.logger.success("✅ Database Connection - Successfully Disposed!")

    except AttributeError as e:
        loguru.logger.warning(f"Database engine already disposed: {e}")

    except Exception as e:
        loguru.logger.error(f"Error while closing database connections: {e}")
