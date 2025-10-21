import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, LargeBinary, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

def uid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    dek_encrypted: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))

    vault_items: Mapped[list["VaultItem"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")

class VaultItem(Base):
    __tablename__ = "vault_items"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    website_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    secret_ciphertext: Mapped[str] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))

    user: Mapped["User"] = relationship(back_populates="vault_items")

    __table_args__ = (
        Index("ix_vault_items_user_name", "user_id", "name"),
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    jti: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")