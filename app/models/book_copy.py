from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    is_borrowed = Column(Boolean, default=False)

    # Relationships
    book = relationship("Book", back_populates="copies")
    borrow_record = relationship("BorrowRecord", back_populates="book_copy", uselist=False)
