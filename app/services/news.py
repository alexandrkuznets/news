from fastapi import HTTPException, Depends
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import date

from app.models.news import News
from app.database.config_db import get_session, sync_session
from app.schemas.news import NewsCreate


async def get_one_news(id_news: int, session: AsyncSession = Depends(get_session)) -> News:
    """
    Возвращает новость из БД по заданному id

    Если новость не найдена возвращает HTTP 404

    Параметры:
    - id: идентификатор новости
    - session: зависимость для асинхронной сессии БД

    Возвращает:
    - Объект новости (News)
    """
    try:
        result = await session.execute(select(News).where(News.id == id_news))
        news = result.scalar_one_or_none()
        if news is None:
            raise HTTPException(status_code=404, detail="News not found")
        return news
    except SQLAlchemyError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def get_news(
        limit: int = 10,
        skip: int = 0,
        source: Optional[str] = None,
        query: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        session: AsyncSession = Depends(get_session)
):
    """
    Возвращает новости из БД по заданным фильтрам

    Параметры:
    - limit: количество записей на странице
    - skip: номер страницы
    - source: фильтрация по источнику
    - query: фильтрация по словам в заголовке и в теле новостей
    - from_date: фильтрация по дате публикации (начиная с даты)
    - to_date: фильтрация по дате публикации (заканчивая датой)
    - session: зависимость для асинхронной сессии БД
    """
    try:
        stmt = select(News).order_by(
            News.published_at).offset(skip).limit(limit)
        if source is not None:
            stmt = stmt.where(News.source == source)
        if query is not None:
            stmt = stmt.where(or_(News.title.contains(query), News.content.contains(query)))
        if from_date is not None:
            stmt = stmt.where(News.published_at > from_date)
        if to_date is not None:
            stmt = stmt.where(News.published_at < to_date)
        result = await session.execute(stmt)
        list_news = result.scalars().all()
        return list_news
    except SQLAlchemyError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def create_news(request: NewsCreate, session: AsyncSession = Depends(get_session)):
    """
    Добавляет новость в БД

    Параметры:
    - request: Объект новости (NewsCreate)
    - session: зависимость для асинхронной сессии БД
    """
    try:
        news = News(
            title=request.title,
            content=request.content,
            source=request.source,
            url=request.url,
            published_at=request.published_at
        )
        session.add(news)
        await session.commit()
        await session.refresh(news)
        return news
    except SQLAlchemyError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(ex))


async def create_bulk_news(list_news: List[NewsCreate], session: AsyncSession = Depends(get_session)):
    """
    Массово добавляет новости в БД

    Параметры:
    - list_news: список объектов новости (NewsCreate)
    - session: зависимость для асинхронной сессии БД
    """
    try:
        session.add_all(list_news)
        await session.commit()
        return list_news
    except SQLAlchemyError as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(ex))


def create_bulk_news_sync(list_news: List[NewsCreate]):
    """
    Массово добавляет новости в БД

    Параметры:
    - list_news: список объектов новости (NewsCreate)
    """
    try:
        sync_session.add_all(list_news)
        sync_session.commit()
    except SQLAlchemyError as ex:
        sync_session.rollback()
        raise HTTPException(status_code=400, detail=str(ex))
