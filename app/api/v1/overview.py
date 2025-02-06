from datetime import datetime
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db  # Import database session
from app.models.book import Book
from app.models.book_copy import BookCopy, BookStatus
from app.models.user import User, UserRole  # Import necessary models
from app.models.reservation import Reservation, ReservationStatus  # Import necessary models
from app.models.borrowing import BorrowRecord

router = APIRouter()

@router.get("/overview", response_model=dict)
def get_overview_data(db: Session = Depends(get_db)):
    total_books = db.query(Book).count()
    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == UserRole.student).count()
    total_reservations = db.query(Reservation).count()
    pending_reservations = db.query(Reservation).filter(Reservation.status == ReservationStatus.PENDING).count()
    overdue_books = db.query(BorrowRecord).filter(BorrowRecord.due_date < datetime.now(), BorrowRecord.returned_date == None).count()
    total_borrowed_books = db.query(BookCopy).filter(BookCopy.status == BookStatus.BORROWED).count()
    total_available_books = db.query(BookCopy).filter(BookCopy.status == BookStatus.AVAILABLE).count()
    

    return {
        "totalBooks": total_books,
        "totalUsers": total_users,
        "totalReservations": total_reservations,
        "pendingReservations": pending_reservations,
        "overdueBooks": overdue_books,
        "totalBorrowedBooks": total_borrowed_books,
        "total_students" : total_students,
        "total_available_books" : total_available_books
    }

@router.get("/student/overview")
def get_student_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Get borrowed books count for the student
    books_borrowed = db.query(BorrowRecord).filter(BorrowRecord.user_id == current_user.id, BorrowRecord.returned_date == None).count()

    # Get reserved books count
    books_reserved = db.query(Reservation).filter(
        Reservation.user_id == current_user.id, Reservation.status == ReservationStatus.PENDING
    ).count()

    # Get overdue books count
    overdue_books = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == current_user.id, BorrowRecord.due_date < datetime.utcnow()
    ).count()

    # Get pending reservations
    pending_reservations = db.query(Reservation).filter(
        Reservation.user_id == current_user.id, Reservation.status == ReservationStatus.PENDING
    ).count()

    return {
        "booksBorrowed": books_borrowed,
        "booksReserved": books_reserved,
        "overdueBooks": overdue_books,
        "pendingReservations": pending_reservations
    }