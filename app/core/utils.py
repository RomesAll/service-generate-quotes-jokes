import jwt, bcrypt
from app.core import settings
from datetime import datetime, timedelta, timezone

def encode_jwt(payload: dict, private_key=settings.auth_jwt.private_key_path.read_text(),
               algorithm=settings.auth_jwt.algorithm, exp=settings.auth_jwt.access_token_exp):
    update_payload = payload.copy()
    update_payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(minutes=exp)
    encoded_jwt = jwt.encode(update_payload, private_key, algorithm=algorithm)
    return encoded_jwt

def decode_jwt(token, public_key=settings.auth_jwt.public_key_path.read_text(),
               algorithm=settings.auth_jwt.algorithm):
    decoded_token = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded_token

def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)