from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.user import UserRead
from app.services.notifications import get_notifications, mark_read

router = APIRouter()

@router.get("/user")
def get_user_notifications(current_user: UserRead = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications = get_notifications(db, current_user.id)
    return notifications

@router.put("/read/{not_id}")
def mark_as_read(not_id:int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    return mark_read(db, current_user.id, not_id)