from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from app.db.base import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    genre = Column(String(50), nullable=True)
    department = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=False, default="jahgajhghj.png")
   

    # borrow_records = relationship("Borrow", back_populates="book")
    # Relationships
    copies = relationship("BookCopy", back_populates="book", lazy="joined")
    reservations = relationship("Reservation", back_populates="book", cascade="all, delete-orphan")
    @property
    def available_copies(self):
        return sum(1 for copy in self.copies if copy.status.value == "available")
    

    