from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Text, DateTime
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    create_at = Column(DateTime, default = datetime.utcnow())
    is_read = Column(Boolean, default=False)
    