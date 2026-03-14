from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, DateTime, func
import uuid
import os


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://reroute:changeme@localhost/reroute"
    ),
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
