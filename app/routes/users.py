# FastAPI
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
# ORM
from sqlalchemy.orm import Session
# System
from datetime import timedelta
from typing import Annotated
# Custom 
from app.db import  models
from app.schemas import user as schemas
from app.db.base import get_session
from app.config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.auth import( is_email_or_username_taken,get_current_user,
        create_access_token, get_password_hash,authenticate_user)
from app.schemas.auth import Token, TokenEncode
from app import constants as global_constant
from app.routes.constants import RoutingPoints, RoutingCategory, ErrorMessages
user_route = APIRouter()

@user_route.post(RoutingPoints.CREATE_USER, tags=[RoutingCategory.AUTH])
async def create(user:schemas.UserCreate,  session:Session = Depends(get_session)):    
    if validate_entity := is_email_or_username_taken(user.email,user.username, models.user.User,session):
        raise HTTPException(status_code=400, detail=f'{validate_entity} is already taken')    
    new_user = models.user.User(email = user.email,username= user.username,
                        _password_hash = get_password_hash(user.password) )  
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=TokenEncode(sub = user.username), expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type=global_constant.TokenType.BEARER)
@user_route.post(RoutingPoints.LOGIN_USER, tags=[RoutingCategory.AUTH] )
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
        session: Session = Depends(get_session) 
    ) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INCORRECT_CREDENTIALS,
            headers=global_constant.AUTH_HEADER,
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=TokenEncode(sub =user.username), expires_delta=access_token_expires
    )    
    return Token(access_token=access_token, token_type=global_constant.TokenType.BEARER)
    
@user_route.get(RoutingPoints.GET_USER, response_model=schemas.User,tags=[RoutingCategory.VIEW])
async def read_users_me(current_user: Annotated[schemas.User,Depends(get_current_user)]):
    return current_user