"""
Pydantic schemas for auth-related operations.
"""
from pydantic import BaseModel
from datetime import datetime
class SessionData(BaseModel):
    username: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenEncode(BaseModel):
    sub: str | None  = None
    exp:datetime | None  = None