"""
Defines the base class for database ORM models.
"""

from app.config.settings import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# # SQLite setup

engine = create_engine(SQLALCHEMY_DATABASE_URL)
print(SQLALCHEMY_DATABASE_URL)
# # Postgres setup

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BASE ORM Model 
Base = declarative_base()

Base.metadata.create_all(bind=engine) 

# DB Utilities 
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()