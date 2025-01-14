from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    ISBN = Column(String(13), nullable=False, unique=True)
    genre = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    copies_available = Column(Integer, default=1)
    