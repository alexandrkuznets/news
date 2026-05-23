from fastapi import HTTPException
from typing import List
import requests
import aiohttp
import asyncio
from datetime import datetime

from app.config import API_KEY
from app.models.news import News

URL = "https://gnews.io/api/v4/top-headlines?category=general&lang=ru&max=10&apikey="


def convert_to_model(answer_api) -> List[News]:
    """
    Создает список объектов новости по полученному ответу от API

    Параметры:
    - answer_api: ответ от API

    Возвращает:
    - Список объектов новости (News)

    """
    news_list = []
    try:
        for elem in answer_api["articles"]:
            news = News(
                title=elem["title"],
                content=elem["content"],
                source=elem["source"]["name"],
                url=elem["url"],
                published_at=datetime.strptime(elem["publishedAt"][:10], "%Y-%m-%d")
            )
            news_list.append(news)
        return news_list
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def fetch_news_from_api():
    """
    Асинхронно делает GET‑запрос к внешнему API и возвращает список новостей.

    Запрашивает данные по URL с подставленным API‑ключом, в случае ошибки
    выбрасывает HTTP‑исключение. Преобразует JSON‑ответ в список объектов новостей через convert_to_model.

    Возвращает:
    Список новостей
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}{API_KEY}") as response:
            response.raise_for_status()
            result = await response.json()
            return convert_to_model(result)


def fetch_news_from_api_sync():
    """
    Синхронно делает GET‑запрос к внешнему API и возвращает список новостей.

    Запрашивает данные по URL с подставленным API‑ключом, в случае ошибки
    выбрасывает HTTP‑исключение. Преобразует JSON‑ответ в список объектов новостей через convert_to_model.

    Возвращает:
    Список новостей
    """
    response = requests.get(f"{URL}{API_KEY}", timeout=10)
    response.raise_for_status()
    result = response.json()
    return convert_to_model(result)

