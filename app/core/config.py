from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Library Management System"
    SQLALCHEMY_DATABASE_URL: str = Field(..., env="SQLALCHEMY_DATABASE_URL")
    ENVIRONMENT: str = Field(..., env="ENVIRONMENT")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
    
try:
    Settings = Settings()
except ValidationError as e:
    print("Environment variables validation error:", e)