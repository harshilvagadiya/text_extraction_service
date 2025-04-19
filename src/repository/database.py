from typing import AsyncGenerator

from loguru import logger
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine as SQLAlchemyAsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as create_sqlalchemy_async_engine
from sqlalchemy.pool import Pool as SQLAlchemyPool

from src.config.manager import settings


class AsyncDatabase:
    def __init__(self):
        self.postgres_uri: str = (
            f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:"
            f"{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:"
            f"{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}"
        )

        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=False,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            pool_pre_ping=True,
            pool_recycle=settings.DB_POOL_RECYCLE,
            pool_timeout=settings.DB_TIMEOUT,
        )

        self.async_session: SQLAlchemyAsyncSession = SQLAlchemyAsyncSession(
            bind=self.async_engine
        )
        self.pool: SQLAlchemyPool = self.async_engine.pool

        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            class_=SQLAlchemyAsyncSession,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[SQLAlchemyAsyncSession, None]:
        """
        Provides a new SQLAlchemy async session.
        """
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @property
    def set_async_db_uri(self) -> str | PostgresDsn:
        return (
            self.postgres_uri.replace("postgresql://", "postgresql+asyncpg://")
            if self.postgres_uri
            else self.postgres_uri
        )


async_db: AsyncDatabase = AsyncDatabase()
