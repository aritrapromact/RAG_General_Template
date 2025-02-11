"""
Pydantic schemas for user-related operations.
"""
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    '''Schemas to validate User to match with Database Table'''
    user_id:int
    username: str
    email: str
    class Config:
        '''match ORM model'''
        from_attribute = True

class UserCreate(BaseModel):
    '''Schemas to validate User Data on Post Request'''
    username: str
    email: EmailStr
    password:str
