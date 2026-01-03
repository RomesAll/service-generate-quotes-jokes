from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas import PaginationJokesSchema, SearchJokesSchema, CredentialsUserSchema, UsersSchemaGET
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

def validate_user_info(request: Request, cred: CredentialsUserSchema, session: Session = Depends(get_session)):
    user = UsersRepository(session, request.client.host).select_users_by_username(cred.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    if not verify_password(cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return UsersSchemaGET.model_validate(user, from_attributes=True)

def validate_access_token(token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    if not token.credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
    try:
        payload = decode_jwt(token.credentials)
        token_type = payload.get('type', None)
        if token_type is None or token_type == 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type, need access token')
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token error')
    return payload

def validate_refresh_token(token: HTTPAuthorizationCredentials = Depends(http_bearer), session: Session = Depends(get_session)):
    if not token.credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
    try:
        payload = decode_jwt(token.credentials)
        token_type = payload.get('type', None)
        if token_type is None or token_type != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type, need refresh token')
        user = UsersRepository(session, client=None).select_users_by_id(payload.get('sub', None))
        return UsersSchemaGET.model_validate(user, from_attributes=True)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token error')

def validate_active_user(payload = Depends(validate_access_token)):
    if not payload.get('active', None) or not payload.get('active', False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not active')
    return payload

validate_active_user_depends = Annotated[validate_active_user, Depends(validate_active_user)]
validate_refresh_token_depends = Annotated[validate_refresh_token, Depends(validate_refresh_token)]
validate_user_info_depends = Annotated[validate_user_info, Depends(validate_user_info)]
pagination_depends = Annotated[PaginationJokesSchema, Depends(PaginationJokesSchema)]
search_depends = Annotated[SearchJokesSchema, Depends(SearchJokesSchema)]
session_depends = Annotated[Session, Depends(get_session)]