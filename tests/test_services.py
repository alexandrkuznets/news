import json

import pytest
from fastapi import HTTPException
from datetime import date

from app.services.news import get_one_news, get_news, create_news, create_bulk_news
from app.models.news import News
from app.schemas.news import NewsCreate


@pytest.mark.asyncio
async def test_get_one_news(setup_db):
    session = setup_db
    result = await get_one_news(1, session)
    assert result is not None
    assert isinstance(result, News)
    with pytest.raises(HTTPException):
        await get_one_news(2, session)


@pytest.mark.asyncio
async def test_get_news(setup_db):
    session = setup_db
    result = await get_news(session=session)
    assert result is not None
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_create_news(setup_db):
    session = setup_db
    news = NewsCreate(
        title="test",
        content="test",
        source="test",
        url="https://example.com",
        published_at=date(2026, 1, 1),
    )
    result = await create_news(news, session)
    assert result is not None
    assert isinstance(result, News)
    assert result.id
    assert result.content == "test"
    assert result.url == "https://example.com"


@pytest.mark.asyncio
async def test_create_bulk_news(setup_db):
    session = setup_db
    news_list = [
        News(title="test", content="test", source="test",
                   url="https://example.com", published_at=date(2026, 1, 1)),
        News(title="test1", content="test1", source="test1",
                   url="https://example.com", published_at=date(2026, 1, 1)),
    ]
    result = await create_bulk_news(news_list, session)
    assert isinstance(result, list)
    assert len(result) == 2
