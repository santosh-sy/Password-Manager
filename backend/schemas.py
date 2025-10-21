from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Password must not be empty.")
        return v

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserOut(BaseModel):
    id: str
    email: EmailStr

class VaultItemCreate(BaseModel):
    name: str
    username: Optional[str] = None
    secret: str

class VaultItemOut(BaseModel):
    id: str
    name: str
    username: Optional[str] = None