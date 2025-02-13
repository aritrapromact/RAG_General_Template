"""Database ORM models for Chat History."""

from sqlalchemy import JSON, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.config.settings import Base

'''This module contains All the SQLAlchemy Database Schemas or Model
'''

class Conversation(Base):
    __tablename__ = "conversation"
    conversation_id = Column(Integer, primary_key= True,autoincrement=True)
    user_id =  Column(Integer, ForeignKey('user.user_id'), nullable=False)
    history = Column(JSON, nullable=False)
    user = relationship('User', back_populates='conversation')
