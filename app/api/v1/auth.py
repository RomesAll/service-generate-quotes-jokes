from fastapi import APIRouter, Request, Response, Depends
from app.dependencies import validate_user_info_depends, session_depends, validate_refresh_token_depends
from app.core.jwt_tokens import create_access_token, create_refresh_token
from app.services import UsersService, UsersSchemaPOST

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/login")
def login(response: Response, user: validate_user_info_depends):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    response.headers["Authorization"] = f'Bearer {access_token}'
    return {'user_info': user.username, 'access_token': access_token, 'refresh_token': refresh_token}

@router.post("/refresh/token")
def refresh_token(response: Response, user: validate_refresh_token_depends):
    access_token = create_access_token(user=user)
    response.headers["Authorization"] = f'Bearer {access_token}'
    return {'user_info': user.username, 'access_token': access_token}

@router.post("/register")
def register(user_info: UsersSchemaPOST, session: session_depends, request: Request):
    result = UsersService(session, request.client.host).create_users(user_info)
    return {'user added': result}