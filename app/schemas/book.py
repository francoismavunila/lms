from pydantic import BaseModel
from typing import Optional
from app.models.book_copy import BookStatus


class BookCopyBase(BaseModel):
    book_id: int

class BookCopyCreate(BookCopyBase):
    book_id: int

class BookCopyRead(BookCopyBase):
    id: int
    status: BookStatus
    
    class Config:
        from_attributes = True
    

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    image_url: Optional[str] = None
    genre: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    
class BookCreate(BookBase):
    pass
   
    
class BookRead(BookBase):
    id: int
    copies: list[BookCopyRead]
    
    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    genre: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    
    