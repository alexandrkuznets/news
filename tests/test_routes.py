from mock import AsyncMock
import mock
from fastapi.testclient import TestClient
from app.main import app
from tests.common import fetch_news_form_api_mock, get_news_mock, MOCK_DB, get_one_news_mock

client = TestClient(app)


@mock.patch("app.routes.news.fetch_news_from_api", fetch_news_form_api_mock)
@mock.patch("app.routes.news.create_bulk_news")
def test_root_handler_create(m_create_bulk_news: AsyncMock):
    response = client.post(url="/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
    m_create_bulk_news.assert_awaited_once()


@mock.patch("app.routes.news.get_news", get_news_mock)
def test_get_news_handler():
    response = client.get("/news")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(MOCK_DB)


@mock.patch("app.routes.news.get_one_news", get_one_news_mock)
def test_get_news_on_id_handler():
    id_news = 1
    response = client.get(f"/news/{id_news}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data == MOCK_DB[id_news]


def test_create_news_handler():
    news = {
        "title": "test",
        "content": "test",
        "source": "test",
        "url": "example.com",
        "published_at": "2026-01-01"
    }
    response = client.post(url="/create_news", json=news)
    assert response.status_code == 200
