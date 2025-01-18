from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    published_date = Column(String)
    summary = Column(String)
    genre = Column(String)