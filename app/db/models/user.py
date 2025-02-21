'''This module contains All the SQLAlchemy Database Schemas or Model'''

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.settings import Base


class User(Base):
    '''ORM Model for Conversation Table'''
    __tablename__ = "user"
    user_id = Column(Integer, primary_key= True,autoincrement=True)
    username =  Column(String(100),unique=True,nullable=False)
    email = Column(String(100),unique=True, index= True, nullable= False )
    _password_hash = Column(String(200), nullable=False)
    conversation = relationship('Conversation', back_populates='user')

    @property
    def password_hash(self):
        '''Return password hash'''
        return self._password_hash
