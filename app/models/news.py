from sqlalchemy import Column, String, Integer, DateTime

from app.database.config_db import Base


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    source = Column(String)
    url = Column(String)
    published_at = Column(DateTime)

