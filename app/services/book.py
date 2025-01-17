from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from fastapi import HTTPException

def create_book(db:Session, book_data:BookCreate):
    try:
        print(book_data)
        book = Book(**book_data.dict())
        print(book)
        db.add(book)
        db.commit()
        db.refresh(book)
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