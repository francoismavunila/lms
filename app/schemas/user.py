from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.student
    
class UserRead(UserBase):
    id: int
    role: UserRole
    
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    role: str | None = None
    is_active: str | None = None
    
class EmailRequest(BaseModel):
    email: EmailStr