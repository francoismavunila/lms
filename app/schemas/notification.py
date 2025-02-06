from pydantic import BaseModel

class NotificationsBase(BaseModel):
    user_id: int
    title: str
    message: str    

class NotificationCreate(NotificationsBase):
    pass
    

class NotificationRead(NotificationsBase):
    id: int
    is_read: bool
    