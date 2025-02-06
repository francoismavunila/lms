from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.book import Book
from app.models.book_copy import BookCopy
from app.models.borrowing import BorrowHistory
from app.models.user import User
from app.services.book import (borrow_book, create_book, get_books, get_book_id, return_book, update_book, delete_book, search_books)
from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.schemas.borrow import BorrowCreate, BorrowRead
import shutil
import os

router = APIRouter()

@router.post("/books", response_model=BookRead)
def add_book(
    title: str = Form(...),
    author: str = Form(...),
    isbn: str = Form(...),
    genre: str = Form(None),
    department: str = Form(None),
    description: str = Form(None),
    num_copies: int = Form(1),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    book_data = BookCreate(
        title=title,
        author=author,
        isbn=isbn,
        genre=genre,
        department=department,
        description=description,
    )
    
    book = create_book(db, book_data, file_path, num_copies)
    
    # Clean up the temporary file
    os.remove(file_path)
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

@router.post("/borrow/{user_id}/{book_id}", response_model=BorrowRead)
def borrow_a_book(user_id: int, book_id: int, db: Session = Depends(get_db)):
    return borrow_book(db, user_id, book_id)


@router.post("/return/{user_id}/{book_copy_id}", response_model=BorrowRead)
def return_a_book(user_id: int, book_copy_id: int, db: Session = Depends(get_db)):
    return return_book(db, user_id, book_copy_id)

@router.get("/borrow-history")
def get_student_borrow_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Fetch borrow history for the current user
    borrow_history = (
        db.query(BorrowHistory)
        .join(BookCopy, BorrowHistory.book_copy_id == BookCopy.id)
        .join(Book, BookCopy.book_id == Book.id)
        .filter(BorrowHistory.user_id == current_user.id)
        .all()
    )

    # Convert to response format
    history_data = [
        {
            "id": record.id,
            "bookTitle": record.book_copy.book.title,
            "borrowDate": record.borrow_date,
            "dueDate": record.due_date,
            "returnedDate": record.returned_date
        }
        for record in borrow_history
    ]

    return history_data


