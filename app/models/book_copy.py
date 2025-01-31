from sqlalchemy import Column, Integer, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class BookStatus(enum.Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    LOST = "lost"
    DAMAGED = "damaged"

class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE, nullable=False)

    # Relationships
    book = relationship("Book", back_populates="copies")
    borrow_record = relationship("BorrowRecord", back_populates="book_copy", uselist=False)
