from fastapi import (APIRouter,Depends,
        HTTPException, HTTPException, Depends)
from typing import Annotated,List,Dict
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage, HumanMessage
from app.db.base import get_session
from app.db.models import Conversation 
from app.schemas.user import User as UserSchema
from app.core.auth import get_current_user
from app.services.agent import react_agent
from app.schemas.chat import Query
import json 

conversation_routes = APIRouter()

@conversation_routes.get('/conversation/',tags=['chat'] )
async def get_chat(current_user: Annotated[UserSchema, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    try:
        conversation_list = session.query(Conversation).filter(
                    Conversation.user_id==current_user.user_id).all()    
        return conversation_list
    except Exception as e:
        raise HTTPException(status_code=500, detail= f'{e}')
    

    



@conversation_routes.get('/conversation/{conversation_id}',tags=['chat'] )
async def get_chat(conversation_id:int,
                current_user: Annotated[UserSchema, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    try:
        if conversation := session.query(Conversation).filter(
                Conversation.user_id == current_user.user_id).filter(
                Conversation.conversation_id==conversation_id).first():
                return conversation
        else:
            raise HTTPException(status_code=404, detail = "No Conversation is found")
    except :
        raise HTTPException(status_code=404, detail='Conversation not found')
    

@conversation_routes.post('/conversation',tags=['chat'] )
async def ask_question(query:Query, 
                current_user: Annotated[UserSchema,Depends(get_current_user)],
                session:Session=Depends(get_session)):
   
    chat_history= [] 
    chat_history.append(HumanMessage(role="user", content=query.question))
    response = react_agent.invoke(
        {"messages": chat_history},
        config={"configurable": {"thread_id": 42}}
    )
    history = response['messages']
    
   
    chat_history_json = [chat.model_dump() for chat in history]

    conversation = Conversation(user_id=current_user.user_id , history=chat_history_json, )     
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return {'answer': history[-1].content, 'conversation_id':conversation.conversation_id}

@conversation_routes.post('/conversation/{conversation_id}',tags=['chat'] )
async def ask_question(conversation_id : int, query:Query, 
                current_user: Annotated[UserSchema,Depends(get_current_user)],
                session:Session=Depends(get_session)):


    conversation = session.query(Conversation).filter(
            Conversation.conversation_id==conversation_id and
            Conversation.user_id == current_user.user_id).first()    
    # print(type(conversation.history[0]))
    chat_history = conversation.history
    response = react_agent.invoke(
        {"messages": chat_history},
        config={"configurable": {"thread_id": 42}}
    )
    history = response['messages']
    
    chat_history_json = [chat.model_dump() for chat in history]
    conversation.history = chat_history_json
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return {'answer': history[-1].content, 'conversation_id':conversation.conversation_id}