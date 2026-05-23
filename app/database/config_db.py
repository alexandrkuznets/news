from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import DATABASE_URL_ASYNC, DATABASE_URL_SYNC

engine = create_async_engine(DATABASE_URL_ASYNC)
Async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)

sync_engine = create_engine(DATABASE_URL_SYNC)
Session = sessionmaker(bind=sync_engine)
sync_session = Session()

class Base(DeclarativeBase):
    pass

async def get_session():
    """
    Возвращает объект сессии AsyncSession, который используется в обработчиках и сервисах
    """
    async with Async_session() as session:
        yield session