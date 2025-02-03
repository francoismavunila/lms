from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserRead, UserCreate, UserLogin, UserUpdate
from app.services.user import get_user_by_email, create_user, authenticate_user, get_all_users, get_user_by_id, update_user
from app.core.security import create_access_token, get_current_user

router = APIRouter()


@router.post("/register", response_model = UserRead)
def register_user(user:UserCreate, db: Session = Depends(get_db)):
    print(user)
    user_db = get_user_by_email(db, user.email)
    if user_db:
        raise HTTPException(
            status_code = 400,
            detail = "Email already registered",
        )
    return create_user(db, user)

@router.post("/login")
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail= "Invalid credentials"
        )
    access_token = create_access_token(data={"sub":user.email})
    return {"access_token":access_token, "token_type": "bearer"}

@router.get("/users", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.get("/user", response_model= UserRead)
def get_user(current_user: UserRead = Depends(get_current_user)):
    return current_user

@router.patch("/users/{user_id}", response_model=UserRead)
def edit_user(user_id:int,  user_update: UserUpdate, db: Session = Depends(get_db)):
    print("am here")
    user = update_user(db, user_id, user_update)
    
    if not user:
        raise HTTPException(status_code=404, detail="not found")
    return user