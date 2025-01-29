from pydantic import BaseModel
from datetime import datetime

class BorrowBase(BaseModel):
    book_id: int
    user_id: int
    
class BorrowCreate(BorrowBase):
    pass

class BorrowRead(BorrowBase):
    id: int
    borrow_date : datetime
    return_date : datetime
    returned : bool
    
    class Config:
        from_attributes = True
        
class BorrowUpdate(BaseModel):
    return_date: datetime
    returned : bool