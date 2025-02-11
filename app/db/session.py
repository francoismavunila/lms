from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings

if Settings.ENVIRONMENT == 'production':
    engine = create_engine(Settings.SQLALCHEMY_DATABASE_URL)
else:
    engine = create_engine(Settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()