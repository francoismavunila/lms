from pydantic import BaseModel

class InventoryRead(BaseModel):
    book_id: int
    title: str
    available_copies: int

    class Config:
        orm_mode = True
