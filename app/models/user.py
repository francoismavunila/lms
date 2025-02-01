from sqlalchemy import Column, String, Integer, Boolean, Enum as SQLAlchemyEnum
from app.db.base import Base
from enum import Enum
from sqlalchemy.orm import relationship

class UserRole(str, Enum):
    student = "student"
    faculty = "faculty"
    librarian = "librarian"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.student)  # Roles: student, faculty, librarian, admin
    
    borrow_records = relationship("BorrowRecord", back_populates="user")
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")