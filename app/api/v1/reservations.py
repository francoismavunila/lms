from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.borrowing import BorrowRecord
from app.models.reservation import Reservation, ReservationStatus
from app.models.book import Book
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.core.security import get_current_user
from app.db.session import get_db
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.post("/reserve", response_model=ReservationRead)
def place_reservation(reservation_data: ReservationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == reservation_data.book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.available_copies > 0:
        raise HTTPException(status_code=400, detail="Book is available, no need to reserve")
    # check if book has been reserved by this user before
    # check if you already borrowed this book
    existing_borrow = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == current_user.id,
        BorrowRecord.book_copy.has(book_id=book.id),
        BorrowRecord.returned_date == None
    ).first()
    
    if existing_borrow:
        raise HTTPException(status_code=400, detail="You can't reserve a book you already borrowed")
    existing_reservation = db.query(Reservation).filter(Reservation.book_id == book.id, Reservation.user_id == current_user.id, Reservation.status == ReservationStatus.PENDING).first()
    if existing_reservation:
        raise HTTPException(status_code=400, detail="You have already reserved this book")
    reservation = Reservation(
        user_id=current_user.id,
        book_id=book.id,
        status=ReservationStatus.PENDING,
        reserved_at=datetime.utcnow()
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

@router.get("/reservations")
def get_user_reservations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).options(joinedload(Reservation.book)).all()

@router.get("/")
def get_all_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).options(
        joinedload(Reservation.book),
        joinedload(Reservation.user)
    ).all()

@router.patch("/reservations/{reservation_id}/cancel", response_model=ReservationRead)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id, Reservation.user_id == current_user.id).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status != ReservationStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot cancel a completed or already canceled reservation")

    reservation.status = ReservationStatus.CANCELED
    db.commit()
    db.refresh(reservation)
    return reservation
