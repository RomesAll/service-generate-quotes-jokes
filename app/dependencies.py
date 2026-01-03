from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas import PaginationJokesSchema, SearchJokesSchema
from app.core.utils import decode_jwt, verify_password
from app.repository import UsersRepository
from app.database import session_maker
from sqlalchemy.orm import Session
from typing import Annotated
import jwt

http_bearer = HTTPBearer()

def get_session():
    try:
        session = session_maker()
        yield session
    finally:
        session.close()

def validate_user_info(username: str, password: str, request: Request, session: Session = Depends(get_session)):
    user = UsersRepository(session, request.client.host).select_users_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user

def validate_token(token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    if not token.credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
    try:
        payload = decode_jwt(token.credentials)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token error')
    return payload

def validate_active_user(payload = Depends(validate_token)):
    if not payload.get('active', None) or not payload.get('active', False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not active')
    return payload

validate_active_user_depends = Annotated[validate_active_user, Depends(validate_active_user)]
validate_user_info_depends = Annotated[validate_user_info, Depends(validate_user_info)]
pagination_depends = Annotated[PaginationJokesSchema, Depends(PaginationJokesSchema)]
search_depends = Annotated[SearchJokesSchema, Depends(SearchJokesSchema)]
session_depends = Annotated[Session, Depends(get_session)]