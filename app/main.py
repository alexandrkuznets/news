import uvicorn
from fastapi import FastAPI

from app.routes.news import router as news_router
from app.tasks import task_download_news
from app.models.news import News
from app.database.config_db import Base

app = FastAPI()

app.include_router(news_router)


if __name__=='__main__':
    uvicorn.run("main:app", reload=True)