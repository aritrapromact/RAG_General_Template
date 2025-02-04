"""
This file contains configuration settings for the application,
such as environment variables and constants.
"""
import os
from pathlib import Path
from dotenv import main
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

main.load_dotenv()

def load_env_var_strict(name: str) -> str:
    """Loads an environment variable and raises an error if not set."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value
## Loading Environment Variables
JWT_AUTH_SECRET_KEY = load_env_var_strict('JWT_AUTH_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 50

## Configuration Settings
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
BASE_DIR = Path(__file__).resolve().parent.parent

if DB_TYPE == "postgres":
    # PostgreSQL Database Configuration
    POSTGRES_USER = load_env_var_strict('POSTGRES_USER')
    POSTGRES_DATABASE = load_env_var_strict('POSTGRES_DATABASE')
    POSTGRES_PASSWORD = load_env_var_strict('POSTGRES_PASSWORD')
    POSTGRES_HOST = load_env_var_strict('POSTGRES_HOST')
    POSTGRES_PORT = load_env_var_strict('POSTGRES_PORT')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
else:
    # SQLite Database Configuration
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/db.sqlite3"

# ORM Engine Configuration

GROQ_API_KEY = load_env_var_strict('GROQ_INFERENCE_API_KEY')
GROQ_MODEL_NAME  = "mixtral-8x7b-32768"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if DB_TYPE == "sqlite" else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base ORM Model
Base = declarative_base()
Base.metadata.create_all(bind=engine)

# DB Utilities
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
