from sqlalchemy.orm import Session
from app.models.user import User

def borrow_book(db:Session, user_id: int, book_id: int):
    # check if user is eligible to borrow another book
    
    # check if the book is available
    # borrow book
    pass

def check_eligibility(db:Session, user_id:int, book_id:int)-> bool:
    # check if user has borrowed the maximum number of books
    max_borrow = 3
    borrowed_books = db.query(User).filter(User.id == user_id).first().borrowed_books
    # check if user has returned all borrowed books
    return True