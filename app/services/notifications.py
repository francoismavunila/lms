from sqlalchemy.orm import Session
from app.models.notifications import Notification
from app.schemas.notification import NotificationCreate
from app.models.notifications import Notification
from fastapi import HTTPException



def create_notification(db:Session, user_id: int, not_data: NotificationCreate):
    new_notification = Notification(
        user_id = user_id,
        title = not_data["title"],
        message = not_data["message"]
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    
    return {"message": "Notification created"}

def get_notifications(db: Session, user_id:int):
    notifications = db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.create_at.desc()).all()
    return notifications

def mark_read(db:Session, user_id: int, not_id: int):
    notification = db.query(Notification).filter(Notification.id == not_id, Notification.user_id == user_id).first()
    
    if not notification:
        raise HTTPException(
            status_code=400,
            detail= "could not mark as read"
        )
    notification.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}