from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from redis import Redis

from app.database.config_db import get_session
from app.schemas.news import NewsCreate, NewsResponse
from app.services.news import get_news, create_news, get_one_news, create_bulk_news
from app.services.news_fetcher import fetch_news_from_api

router = APIRouter()


@router.post("/")
async def root_handler_create(session: AsyncSession = Depends(get_session)):
    """Обработчик POST‑запроса: забирает новости из внешнего API и массово создаёт записи в БД"""
    news_list = await fetch_news_from_api()
    await create_bulk_news(news_list, session)
    return {"status": "OK"}


@router.get("/news")
async def get_news_handler(
        limit: int = 10,
        page: int = 1,
        source: str = None,
        query: str = None,
        from_date: date = None,
        to_date: date = None,
        session: AsyncSession = Depends(get_session)
) -> List[NewsResponse]:
    """Обработчик GET-запроса: возвращает новости из БД по заданным фильтрам

    Параметры:
    - limit: количество записей на странице
    - page: номер страницы
    - source: фильтрация по источнику
    - query: фильтрация по словам в заголовке и в теле новостей
    - from_date: фильтрация по дате публикации (начиная с даты)
    - to_date: фильтрация по дате публикации (заканчивая датой)
    - session: зависимость для асинхронной сессии БД
    """
    result = await get_news(
        limit=limit,
        skip=(page - 1) * limit,
        source=source,
        query=query,
        from_date=from_date,
        to_date=to_date,
        session=session)

    return result


@router.get("/news/{id_news}")
async def get_news_on_id_handler(
        id_news: int,
        session: AsyncSession = Depends(get_session)
) -> NewsResponse:
    """Обработчик GET-запроса: Возвращает новость из БД по id"""
    result = await get_one_news(id_news, session)
    return result


@router.post("/create_news")
async def create_news_handler(
        request: NewsCreate,
        session: AsyncSession = Depends(get_session)
) -> NewsResponse:
    """Обработчик POST-запроса: Создаёт новость в БД по переданным данным

    Параметры:
    request: Новость в JSON формате
    session: зависимость для асинхронной сессии БД
    """
    result = await create_news(request, session)
    return result
