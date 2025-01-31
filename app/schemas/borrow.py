from pydantic import BaseModel
from datetime import datetime

class BorrowBase(BaseModel):
    user_id: int
    book_copy_id: int

class BorrowCreate(BorrowBase):
    pass

class BorrowRead(BorrowBase):
    id: int
    borrow_date: datetime
    due_date: datetime
    returned_date: datetime | None

    class Config:
        from_attributes = True
