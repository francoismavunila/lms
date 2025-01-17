from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    genre: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    
class BookCreate(BookBase):
    copies_available: Optional[int] = None
   
    
class BookRead(BookBase):
    id: int
    copies_available: int
    
    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    genre: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    copies_available: Optional[str] = None
    
    