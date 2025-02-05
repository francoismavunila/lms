from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.inventory import books_stats, get_book_availability, update_book_status
from app.models.book_copy import BookStatus

router = APIRouter()

@router.get("/inventory/{book_id}")
def check_book_availability(book_id: int, db: Session = Depends(get_db)):
    book_info = get_book_availability(db, book_id)
    
    if not book_info:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book_info

@router.patch("/inventory/{book_copy_id}/status/{status}")
def change_book_status(book_copy_id: int, status: BookStatus, db: Session = Depends(get_db)):
    book_copy = update_book_status(db, book_copy_id, status)

    if not book_copy:
        raise HTTPException(status_code=404, detail="Book copy not found")
    
    return {"book_copy_id": book_copy_id, "new_status": status.value}

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return books_stats(db)