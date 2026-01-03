from app.core.utils import encode_jwt
from app.schemas import UsersSchemaGET, UsersSchemaPOST

def create_token(payload: dict, expires_in: int, token_type: str):
    payload.update({'type': token_type})
    token = encode_jwt(payload=payload, expires_in=expires_in)
    return token

def create_access_token(user: UsersSchemaGET):
    payload = {
        'sub': str(user.id),
        'username': user.username,
        'active': user.active,
    }
    return create_token(payload=payload, expires_in=10, token_type='access')

def create_refresh_token(user: UsersSchemaGET):
    payload = {
        'sub': str(user.id),
    }
    return create_token(payload=payload, expires_in=20, token_type='refresh')