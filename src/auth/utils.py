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
