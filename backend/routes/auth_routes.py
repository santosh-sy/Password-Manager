from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Depends, status
from sqlalchemy.orm import Session
from backend.schemas import LoginRequest, TokenPair, AccessToken, UserOut
from backend.users_repo import get_user_by_email, create_user
from backend.security import verify_password, create_access_token, decode_access_token
from backend.config import settings
from backend.dependencies import get_current_user
from backend.database import get_db
from backend.rate_limit import allow_login
from backend.models import RefreshToken, User
import time

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(payload: LoginRequest, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, payload.email, payload.password)
    return UserOut(id=user.id, email=user.email)

@router.post("/login", response_model=TokenPair)
def login_user(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "unknown"
    if not allow_login(ip):
        raise HTTPException(status_code=429, detail="Too many login attempts")

    user = get_user_by_email(db, payload.email)
    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        time.sleep(0.25)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, _ = create_access_token(
        sub=user.email, scope="access", expires_in_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    refresh_token, jti = create_access_token(
        sub=user.email, scope="refresh", expires_in_seconds=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )
    # persist refresh token metadata
    db.add(RefreshToken(
        user_id=user.id,
        jti=jti,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    ))
    db.commit()
    return TokenPair(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenPair)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    # Validate incoming refresh token
    try:
        data = decode_access_token(refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if data.get("scope") != "refresh":
        raise HTTPException(status_code=401, detail="Wrong token scope")

    user: User | None = db.query(User).filter(User.email == data["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Check jti not revoked/expired and exists
    token_rec: RefreshToken | None = db.query(RefreshToken).filter(RefreshToken.jti == data["jti"]).first()
    if not token_rec or token_rec.revoked or token_rec.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token revoked/expired")

    # ROTATE: revoke old, issue new pair
    token_rec.revoked = True
    access_token, _ = create_access_token(
        sub=user.email, scope="access", expires_in_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    new_refresh_token, new_jti = create_access_token(
        sub=user.email, scope="refresh", expires_in_seconds=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )
    db.add(RefreshToken(
        user_id=user.id,
        jti=new_jti,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    ))
    db.commit()
    return TokenPair(access_token=access_token, refresh_token=new_refresh_token)

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    try:
        data = decode_access_token(refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if data.get("scope") != "refresh":
        raise HTTPException(status_code=401, detail="Wrong token scope")

    rec = db.query(RefreshToken).filter(RefreshToken.jti == data["jti"]).first()
    if rec:
        rec.revoked = True
        db.commit()
    return {"detail": "Logged out"}