from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.book import (create_book, get_books, get_book_id, update_book, delete_book, search_books)
from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter()

@router.post("/books", response_model=BookRead)
def add_book(book_data:BookCreate, db: Session = Depends(get_db)):
    book = create_book(db, book_data)
    return book

@router.get("/books", response_model=list[BookRead])
def get_all_books(skip:int = 0, limit: int = 10,db: Session= Depends(get_db)):
    return get_books(db, skip, limit)


@router.get("/book/{book_id}", response_model=BookRead)
def get_book_by_id(book_id:int, db: Session = Depends(get_db)):
    book = get_book_id(db, book_id)
    
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book

@router.patch("/book/{book_id}", response_model=BookRead)
def edit_book(book_id: int, patch_data: BookUpdate, db: Session = Depends(get_db)):
    patched_book = update_book(db, book_id, patch_data)
    if not patch_data:
        raise HTTPException(
            status_code=404,
            detail="book not found"
        )
    return patched_book

@router.delete("/delete/{book_id}")
def remove_book(book_id:int, db: Session = Depends(get_db)):
    book = delete_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code= 404, 
            detail="book not found"
        )
    return {"message": "Book deleted successfully"}

@router.get("/books/search", response_model=list[BookRead])
def serach_for_books(query: str, db: Session = Depends(get_db)):
    return search_books(db, query)