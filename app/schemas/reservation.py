from pydantic import BaseModel
from datetime import datetime
from app.models.reservation import ReservationStatus

class ReservationCreate(BaseModel):
    book_id: int

class ReservationRead(BaseModel):
    id: int
    book_id: int
    user_id: int
    status: ReservationStatus
    reserved_at: datetime

    class Config:
        from_attributes = True
