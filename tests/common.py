



MOCK_API = [
    {"id": "test", "title": "test", "content": "test"},
]

MOCK_DB = [
    {"id": 1, "title": "test", "content": "test", "source": "test", "url": "example.com", "published_at": "2026-01-01"},
    {"id": 2, "title": "test", "content": "test", "source": "test", "url": "example.com", "published_at": "2026-01-01"},
    {"id": 3, "title": "test", "content": "test", "source": "test", "url": "example.com", "published_at": "2026-01-01"},
]


async def fetch_news_form_api_mock():
    return MOCK_API


async def get_news_mock(*args, **kwargs):
    return MOCK_DB


async def get_one_news_mock(*args, **kwargs):
    return MOCK_DB[1]