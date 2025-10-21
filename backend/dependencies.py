from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict
from security import decode_access_token
from database import get_db
from sqlalchemy.orm import Session
from models import User

bearer = HTTPBearer(auto_error=True)

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
        db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("scope") != "access":
        raise HTTPException(status_code=401, detail="Wrong token scope")
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or missing user")
    return user