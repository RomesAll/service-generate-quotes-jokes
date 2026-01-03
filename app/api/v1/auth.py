from fastapi import APIRouter, Request, Response
from app.dependencies import validate_user_info_depends
from app.dependencies import session_depends
from app.core.utils import encode_jwt
from app.services import UsersService
from app.schemas import UsersSchemaPOST

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login")
def login(response: Response, user: validate_user_info_depends):
    payload = {
        'sub': str(user.id),
        'username': user.username,
        'active': user.active
    }
    token = encode_jwt(payload)
    response.headers["Authorization"] = f'Bearer {token}'
    return {'message': payload, 'access token': token}

@router.post("/register")
def register(user_info: UsersSchemaPOST, session: session_depends, request: Request):
    result = UsersService(session, request.client.host).create_users(user_info)
    return {'user added': result}