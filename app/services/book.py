from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.book import Book
from app.models.book_copy import BookCopy, BookStatus
from app.models.borrowing import BorrowRecord
from app.schemas.book import BookCreate, BookUpdate
from fastapi import HTTPException

def create_book(db:Session, book_data:BookCreate, num_copies: int=1):
    try:
        print(book_data)
        book = Book(**book_data.dict())
        print(book)
        db.add(book)
        db.commit()
        db.refresh(book)
        for _ in range(num_copies):
            book_copy = BookCopy(book_id=book.id)
            db.add(book_copy)
        db.commit()
        return book
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while creating the book") from e
    
def get_books(db: Session, skip:int=0, limit:int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book_id(db: Session, book_id: int ):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book_update: BookUpdate):
    book = get_book_id(db, book_id)
    if not book:
        return None
    
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book
    
def delete_book(db: Session, book_id:int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    
    db.delete(book)
    db.commit()
    return book

def search_books(db: Session, query: str):
    books = db.query(Book).filter(
        Book.title.ilike(f"%{query}%") |
        Book.author.ilike(f"%{query}%") |
        Book.isbn.ilike(f"%{query}%") |
        Book.genre.ilike(f"%{query}%") 
    ).all()
    
    return books

def borrow_book(db: Session, user_id: int, book_id: int):
    book_copy = db.query(BookCopy).filter(
        BookCopy.book_id == book_id, BookCopy.status == BookStatus.AVAILABLE
    ).first()
    
    if not book_copy:
        return None
    
    existing_borrow = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_copy.has(book_id=book_id),
        BorrowRecord.returned_date == None
    ).first()
    
    if existing_borrow:
        return "already_borrowed"  # User already has this book

    # Mark copy as borrowed
    book_copy.status = BookStatus.BORROWED

    # Create borrow record
    borrow_record = BorrowRecord(
        user_id=user_id,
        book_copy_id=book_copy.id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)  # 2-week borrowing period
    )
    
    db.add(borrow_record)
    db.commit()
    db.refresh(borrow_record)
    return borrow_record

def return_book(db: Session, user_id: int, book_copy_id: int):
    borrow_record = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_copy_id == book_copy_id,
        BorrowRecord.returned_date == None
    ).first()

    if not borrow_record:
        return None  # No active borrow record found

    # Mark book copy as available
    book_copy = db.query(BookCopy).filter(BookCopy.id == book_copy_id).first()
    book_copy.status = BookStatus.AVAILABLE

    # Update return date in borrow record
    borrow_record.returned_date = datetime.utcnow()

    db.commit()
    db.refresh(borrow_record)
    return borrow_record