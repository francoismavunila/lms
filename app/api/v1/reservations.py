from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.reservation import Reservation, ReservationStatus
from app.models.book import Book
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter()

@router.post("/reserve", response_model=ReservationRead)
def place_reservation(reservation_data: ReservationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == reservation_data.book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.available_copies > 0:
        raise HTTPException(status_code=400, detail="Book is available, no need to reserve")
    
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

@router.get("/reservations", response_model=list[ReservationRead])
def get_user_reservations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()

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
