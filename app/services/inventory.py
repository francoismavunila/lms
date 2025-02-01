from sqlalchemy.orm import Session
from app.models.book_copy import BookCopy, BookStatus
from app.models.book import Book

def get_book_availability(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    return {"book_id": book_id, "title": book.title, "available_copies": book.available_copies}

def update_book_status(db: Session, book_copy_id: int, status: BookStatus):
    book_copy = db.query(BookCopy).filter(BookCopy.id == book_copy_id).first()
    
    if not book_copy:
        return None  # Book copy not found

    book_copy.status = status
    db.commit()
    db.refresh(book_copy)
    return book_copy
