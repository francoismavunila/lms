from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.db.base import Base

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_copy_id = Column(Integer, ForeignKey("book_copies.id"), nullable=False, unique=True)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    returned_date = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="borrow_records")
    book_copy = relationship("BookCopy", back_populates="borrow_record")

class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_copy_id = Column(Integer, ForeignKey("book_copies.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    returned_date = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User")
    book_copy = relationship("BookCopy")
