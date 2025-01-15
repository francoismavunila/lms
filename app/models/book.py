from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    genre = Column(String(50), nullable=True)
    department = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    copies_available = Column(Integer, default=1)

    