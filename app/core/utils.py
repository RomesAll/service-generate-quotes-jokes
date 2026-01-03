from app.core import settings
from datetime import datetime, timedelta, timezone
import jwt, bcrypt

def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password)

def encode_jwt(payload: dict,
               expires_in = settings.auth_jwt.access_token_exp,
               algorithm = settings.auth_jwt.algorithm,
               private_key = settings.auth_jwt.private_key_path.read_text()):
    updated_payload = payload.copy()
    updated_payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_in)
    encoded_jwt = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded_jwt

def decode_jwt(token,
               public_key = settings.auth_jwt.public_key_path.read_text(),
               algorithm = settings.auth_jwt.algorithm):
    decoded_jwt = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded_jwt