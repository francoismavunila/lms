from app.db.base import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
class Borrow(Base):
    __tablename__ = "borrows"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", nullable = False))
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    return_date = Column(DateTime, default = lambda: datetime.utcnow() + timedelta(days=14), nullable=False)
    returned = Column(Boolean, default= False, nullable=False)
    
        # Relationships
    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrow_records")