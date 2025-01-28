"""
Defines authentication-related API endpoints.
"""
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session 
from pydantic import EmailStr 
from jose import JWTError, jwt
from typing import Annotated
from app.db.models.user import User
from app.db.base import Base, get_session
from app.config.settings import JWT_AUTH_SECRET_KEY,ALGORITHM
from datetime import timedelta,timezone,datetime
from app.core import constants as core_constant
from app import constants as global_constant
from app.schemas.auth import TokenEncode
from app.routes.constants import RoutingPoints

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=RoutingPoints.LOGIN_USER)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def is_email_or_username_taken(email: EmailStr,
            username:str, model:Base , session:Session ) -> bool | str:
    '''check in database the given email is already exist or not
    input:
        email : Email String
        model : model or table where to check
        session : SQLAlchemy Database Session Utility 
    return str: 
        return 'email' if email exist 
        return 'username' if username exist 
        return None for new user 
    '''
    existing_object = session.query(model).filter_by(email=email).first()
    if existing_object  : 
        return core_constant.USER_ID.EMAIL 
    existing_object = session.query(model).filter_by(username=username).first()
    if existing_object:
        return core_constant.USER_ID.USERNAME
    return False
    
## Helper Functions 
def verify_password(plain_password, hashed_password):
    """Password Verification by converting Hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Return Hash of any string """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, session:Session):
    """Authenticated an user"""
    if user := session.query(User).filter_by(username=username).first():
        return user if verify_password(password, user._password_hash) else False
    else: return False


def create_access_token(data: TokenEncode, expires_delta: timedelta | None = None):
    """Create Access Token usning Openssl Secret key """
    if not isinstance(data, TokenEncode):
        raise TypeError(global_constant.GEBNERAL_TYPE_ERROR.format(type(TokenEncode)))
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data.exp  = expire
    return  jwt.encode(data.model_dump(), JWT_AUTH_SECRET_KEY, algorithm=ALGORITHM)



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],session:Session=Depends(get_session)):
    """Authenticate user and return current user if authentication success"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=core_constant.MSG_INVALID_CREDENTIALS,
        headers=global_constant.AUTH_HEADER,
    )
    try:
        payload = jwt.decode(token, JWT_AUTH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if user := session.query(User).filter_by(username=username).first():
        return user
    raise credentials_exception
    