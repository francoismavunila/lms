from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.book_copy import BookCopy
from app.models.borrowing import BorrowRecord
from app.schemas.user import UserCreate, UserUpdate, EmailRequest
from app.core.security import verify_password, get_password_hash
from app.models.user import User
from sqlalchemy.orm import joinedload

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db:Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return user

def create_user(db:Session, user: UserCreate):
    try:
        # create a password hash
        hashed_password = get_password_hash(user.password)
        
        # create a user object
        db_user = User(username = user.username, email=user.email, hashed_password = hashed_password, role = user.role)
        
        # stage 
        db.add(db_user)
        # commit
        db.commit()
        
        db.refresh(db_user)
        
        return db_user
    
    except IntegrityError:
        print("user with this email or username already exist..")
        raise HTTPException(
            status_code=400,
            detail = "user with this email or username already exist.."
        )
    
    except Exception as e:
        print(f"An unexpected error occured {str(e)}")
        raise HTTPException(
            status_code = 500,
            detail = f"An unexpected error occured {str(e)}"
        )

def get_all_users(db:Session):
    return db.query(User).all()

def authenticate_user(db:Session, email:str, password:str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = get_user_by_id(db, user_id)
    print("am here")
    if not user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def get_user_profile(db: Session, user_email: str):
    student = db.query(User).filter(User.email == user_email).options(
        joinedload(User.borrow_records).joinedload(BorrowRecord.book_copy).joinedload(BookCopy.book)
    ).first()
    if student == None:
        print("am here")
        raise HTTPException(status_code=400, detail="user with this email not found")
    return student