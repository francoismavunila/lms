from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.models.book_copy import BookStatus
import enum

class ReservationStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    reserved_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")
