from sqlalchemy.orm import Session
from app.models.book_copy import BookCopy, BookStatus
from app.models.book import Book
from sqlalchemy import func

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

def books_stats(db: Session):
    # Count total book types
    total_book_types = db.query(func.count(Book.id)).scalar()
    
    # Count total copies
    total_copies = db.query(func.count(BookCopy.id)).scalar()
    
    # Count copies by status
    total_available_copies = db.query(func.count(BookCopy.id)).filter(BookCopy.status == BookStatus.AVAILABLE).scalar()
    total_borrowed_copies = db.query(func.count(BookCopy.id)).filter(BookCopy.status == BookStatus.BORROWED).scalar()
    total_lost_copies = db.query(func.count(BookCopy.id)).filter(BookCopy.status == BookStatus.LOST).scalar()
    total_damaged_copies = db.query(func.count(BookCopy.id)).filter(BookCopy.status == BookStatus.DAMAGED).scalar()
    
    return {
        "total_book_types": total_book_types,
        "total_copies": total_copies,
        "total_available_copies": total_available_copies,
        "total_borrowed_copies": total_borrowed_copies,
        "total_lost_copies": total_lost_copies,
        "total_damaged_copies": total_damaged_copies,
    }
    