import time
import uuid
import jwt
from typing import Any, Dict, Optional
from passlib.context import CryptContext
from backend.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str, scope: str, expires_in_seconds: int) -> tuple[str, str]:
    now = int(time.time())
    jti = str(uuid.uuid4())
    payload = Dict[str, Any] = {
        "sub": sub, "scope": scope, "iat": now, "exp": now + expires_in_seconds,
        "iss": settings.APP_NAME, "jti": jti
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, jti

def decode_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])