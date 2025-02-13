from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.logging_config import logger
from app.config.settings import get_session
from app.constants import LoggingMessages
from app.core.auth import get_current_user
from app.db.models import Conversation
from app.routes.constants import ErrorMessages, RoutingCategory, RoutingPoints
from app.schemas.chat import AIChat, ChatResponse, HumanChat, Query
from app.schemas.user import User as UserSchema
from app.services.RAG.llm_search import get_llm_response

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
    response = get_llm_response(query.question, current_user.user_id)

    chat_history += [
        HumanChat(content=response['query']),
        AIChat(content=response['answer'],resources=response['references'])
    ]
    chat_history_json = [chat.model_dump() for chat in chat_history]
    conversation = Conversation(user_id=current_user.user_id , history=chat_history_json)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return ChatResponse(answer=response['answer'], references= response['references'], conversation_id=conversation.conversation_id)



@conversation_routes.post(RoutingPoints.CHAT_CONVERSATION,tags=[RoutingCategory.CONVERSATION ])
async def ask_question(conversation_id : int, query:Query,
                    current_user: Annotated[UserSchema,Depends(get_current_user)],
                    session:Session=Depends(get_session)):
    logger.info(LoggingMessages.START_CONVERSATION)
    conversation = session.query(Conversation).filter(
            Conversation.conversation_id==conversation_id and
            Conversation.user_id == current_user.user_id).first()
    chat_history_json = conversation.history
    response = get_llm_response(query.question, current_user.user_id)
    chat_history = [
        HumanChat(content=response['query']),
        AIChat(content=response['answer'],resources=response['references'])
    ]
    chat_history_json +=  [chat.model_dump() for chat in chat_history]
    conversation.history = chat_history_json
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return ChatResponse(answer=response['answer'],
                        references=response['references'],
                        conversation_id=conversation.conversation_id)
