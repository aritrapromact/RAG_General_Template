"""Database ORM models for Chat History."""

from sqlalchemy import (Column, ForeignKey, Integer, String, JSON)
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

'''This module contains All the SQLAlchemy Database Schemas or Model
'''

class Conversation(Base):
    __tablename__ = "conversation"    
    conversation_id = Column(Integer, primary_key= True,autoincrement=True)
    user_id =  Column(Integer, ForeignKey('user.user_id'), nullable=False)
    history = Column(JSON, nullable=False)
    user = relationship('User', back_populates='conversation')