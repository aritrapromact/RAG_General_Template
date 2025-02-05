from pydantic import BaseModel
from typing import List

class Query(BaseModel):
    question:str

class ChatResponse(BaseModel):
    answer:str
    references : List[dict] | None 
    conversation_id:int