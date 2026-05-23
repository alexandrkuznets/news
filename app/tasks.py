from celery import Celery
from celery.schedules import crontab

from app.celery_app import app
from app.services.news_fetcher import fetch_news_from_api_sync
from app.services.news import create_bulk_news_sync



@app.task()
def task_download_news():
    """
    Celery-задача для запроса к внешнему API и сохранения результата в БД
    """
    news_list = fetch_news_from_api_sync()
    create_bulk_news_sync(news_list)
    return {"result": "Сохранили в БД"}



@app.on_after_configure.connect()
def setup_periodic_task(sender: Celery, **kwargs):
    """
    Установка периодичности выполнения Celery-задач

    Параметры:
    sender: Объект класса Celery

    Добавляет задачу task_download_news на выполнение:
    - каждый день в 7:00;
    - каждый день в 19:00.
    """
    sender.add_periodic_task(crontab(hour=7), task_download_news)
    sender.add_periodic_task(crontab(hour=19), task_download_news)