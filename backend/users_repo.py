from sqlalchemy.orm import Session
from models import User
from security import hash_password
from utils.crypto_utils import generate_user_dek, encrypt_dek_with_mek

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    dek = generate_user_dek()
    dek_encrypted = encrypt_dek_with_mek(dek)
    user = User(email=email, password_hash=hash_password(password), dek_encrypted=dek_encrypted)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user