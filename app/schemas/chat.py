'''Pydantic schemas for chat related operations. '''

from typing import List

from pydantic import BaseModel


class Query(BaseModel):
    '''Query Schema'''
    question:str

class ChatResponse(BaseModel):
    '''Chat Response Schema'''
    answer:str
    references : List[dict|str] | None
    conversation_id:int

class HumanChat(BaseModel):
    role:str = 'USER'
    content:str

class AIChat(BaseModel):
    role:str = 'AI'
    content:str
    resources:List[dict|str] | None