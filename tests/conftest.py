from datetime import date

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.database.config_db import Base
from app.models.news import News

engine = create_async_engine("sqlite+aiosqlite:///:memory:")

Async_session = async_sessionmaker(engine, class_=AsyncSession)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def setup_db():
    await create_table()

    async with Async_session() as session:
        news = News(
            id=1,
            title="test",
            content="test",
            source="test",
            url="https://example.com",
            published_at=date(2026, 1, 1),
        )
        session.add(news)
        await session.commit()
    yield session
    await drop_table()