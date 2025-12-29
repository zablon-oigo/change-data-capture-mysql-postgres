import uuid
import logging
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import HTTPException

import jwt
from passlib.context import CryptContext
from src.config import Config

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, 
    salt="email-configuration"
)

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as jwte:
        logging.exception("JWT decode error", exc_info=jwte)
        return None
    except Exception as e:
        logging.exception("Unknown error decoding JWT", exc_info=e)
        return None



def create_url_safe_token(data: dict) -> str:

    try:
        token = serializer.dumps(data)
        return token
    except Exception as e:
        logging.error(f"Error creating token: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create token")

