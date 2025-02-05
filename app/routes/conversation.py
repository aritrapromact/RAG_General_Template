from fastapi import (APIRouter,Depends,
        HTTPException, HTTPException, Depends)
from pydantic import BaseModel
from typing import Annotated,List,Dict
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage,AIMessage
from app.config.settings import get_session
from app.db.models import Conversation 
from app.schemas.user import User as UserSchema
from app.core.auth import get_current_user
from app.services.agent import agent_executor
from app.routes.constants import RoutingPoints, RoutingCategory, ErrorMessages
from app.schemas.chat import Query, ChatResponse
from app.services.agent import get_resource_from_agent_response 

conversation_routes = APIRouter()

@conversation_routes.get(RoutingPoints.GET_CONVERSATION_LIST,tags=[RoutingCategory.CONVERSATION ])
async def get_chat(current_user: Annotated[UserSchema, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    try:
        conversation_list = session.query(Conversation).filter(
                    Conversation.user_id==current_user.user_id).all()    
        return conversation_list
    except Exception as e:
        raise HTTPException(status_code=500, detail= f'{e}')
    

    



@conversation_routes.get(RoutingPoints.GET_CONVERSATION,tags=[RoutingCategory.CONVERSATION ])
async def get_chat(conversation_id:int,
                current_user: Annotated[UserSchema, Depends(get_current_user)],
                session:Session=Depends(get_session)):
    try:
        if conversation := session.query(Conversation).filter(
                Conversation.user_id == current_user.user_id).filter(
                Conversation.conversation_id==conversation_id).first():
                return conversation
        else:
            raise HTTPException(status_code=404, detail = ErrorMessages.CONVERSATION_NOT_EXIST)
    except :
        raise HTTPException(status_code=404, detail=ErrorMessages.CONVERSATION_NOT_EXIST)
    

@conversation_routes.post(RoutingPoints.CREATE_NEW_CONVERSATION,tags=[RoutingCategory.CONVERSATION ])
async def ask_question(query:Query, current_user: Annotated[UserSchema,Depends(get_current_user)],
                session:Session=Depends(get_session)):
    chat_history= [] 
    response = agent_executor.invoke(
        {
            "input": query.question,
            "chat_history": chat_history
        }
    )
    
    chat_history += [
        HumanMessage(content=response['input']),
        AIMessage(content=response['output'])
    ]
   
    chat_history_json = [chat.model_dump() for chat in chat_history]
    source_reference = get_resource_from_agent_response(response)

    conversation = Conversation(user_id=current_user.user_id , history=chat_history_json, )     
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return ChatResponse(answer=response['output'], references= source_reference, conversation_id=conversation.conversation_id)

@conversation_routes.post(RoutingPoints.CHAT_CONVERSATION,tags=[RoutingCategory.CONVERSATION ])
async def ask_question(conversation_id : int, query:Query, current_user: Annotated[UserSchema,Depends(get_current_user)],
                session:Session=Depends(get_session)):
    conversation = session.query(Conversation).filter(
            Conversation.conversation_id==conversation_id and
            Conversation.user_id == current_user.user_id).first()    
    chat_history = conversation.history
    response = agent_executor.invoke(
        {
            "input": query.question,
            "chat_history": chat_history
        }
    )
    source_reference = get_resource_from_agent_response(response)
    chat_history += [
        HumanMessage(content=response['input']),
        AIMessage(content=response['output'])
    ]
    chat_history_json = [chat.model_dump() if isinstance(chat, BaseModel) else chat for chat in chat_history  ]
    conversation.history = chat_history_json
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return ChatResponse(answer=response['output'],
                        references=source_reference,
                        conversation_id=conversation.conversation_id)