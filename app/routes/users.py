'''This module Contains all Routing Points functions related to Users '''

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import constants as global_constant
from app.config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, get_session
from app.core.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    is_email_or_username_taken,
)
from app.db import models
from app.routes.constants import ErrorMessages, RoutingCategory, RoutingPoints
from app.schemas import user as schemas
from app.schemas.auth import Token, TokenEncode
from app.services.RAG.document_parser import parse_documents
from app.services.RAG.vectorstore import save_on_vector_store

user_route = APIRouter()

@user_route.post(RoutingPoints.CREATE_USER, tags=[RoutingCategory.AUTH])
async def create(user:schemas.UserCreate,  session:Session = Depends(get_session)):
    '''Create New User'''
    if validate_entity := is_email_or_username_taken(user.email,user.username, models.user.User,session):
        raise HTTPException(status_code=400, detail=ErrorMessages.ALREADY_TAKEN.format(validate_entity))
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
    '''Return Access Token for Login User '''

    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INCORRECT_CREDENTIALS,
            headers=global_constant.AUTH_HEADER,
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=TokenEncode(sub = user.username), expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type=global_constant.TokenType.BEARER)

@user_route.get(RoutingPoints.GET_USER, response_model=schemas.User,tags=[RoutingCategory.VIEW])
async def read_users_me(current_user: Annotated[schemas.User,Depends(get_current_user)]):
    return current_user

@user_route.post(RoutingPoints.UPLOAD_DOCUMENT, tags=[RoutingCategory.UPLOAD])
async def upload_file( current_user: Annotated[schemas.User,Depends(get_current_user)],file: UploadFile = File(...)):
    if not file.filename :
        raise HTTPException(status_code=400, detail="File name is empty")
    documents = parse_documents(await file.read(), file.filename, file.content_type,
        file_metadata={'user_name':current_user.username})
    save_on_vector_store(documents,current_user.user_id)
    return {'message':'File uploaded and Index successfully'}

