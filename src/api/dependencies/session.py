import typing
from sqlalchemy.ext.asyncio import (AsyncSession as SQLAlchemyAsyncSession,)
from src.repository.database import async_db


async def get_async_session() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    async_session_factory = async_db.async_session_factory
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()