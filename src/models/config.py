import contextlib
from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from settings.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URI,
    echo=False,
    pool_size=20,
    max_overflow=0,
)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as ex:
            await session.rollback()
            raise ex

context_db_session = contextlib.asynccontextmanager(get_db_session)
