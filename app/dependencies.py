import jwt
from jwt import InvalidTokenError
from starlette import status

from app.database import session_maker
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.base import PaginationJokesSchema, SearchJokesSchema
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.utils import *

def get_session():
    try:
        session = session_maker()
        yield session
    finally:
        session.close()

pagination_depends = Annotated[PaginationJokesSchema, Depends(PaginationJokesSchema)]
search_depends = Annotated[SearchJokesSchema, Depends(SearchJokesSchema)]
session_depends = Annotated[Session, Depends(get_session)]


user_db = {
    'bobuser': {'name': 'bob', 'password': hash_password('qwerty')},
    'nikuser': {'name': 'nik', 'password': hash_password('qwerty123')}
}

http_bearer = HTTPBearer()

def validate_token(token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    if not token.credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
    try:
        payload = decode_jwt(token.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token error')
    return payload

def validate_user_info(username: str, password: str):
    if not username in user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    psw_hashed = hash_password(password)
    if not verify_password(password, psw_hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user_db.get(username)