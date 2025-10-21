import base64
from cryptography.fernet import Fernet
from typing import Tuple
from backend.config import settings

MEK = Fernet(settings.MASTER_ENCRYPTION_KEY.encode() if isinstance(settings.MASTER_ENCRYPTION_KEY, str)
             else settings.MASTER_ENCRYPTION_KEY)

def generate_user_dek() -> bytes:
    """Generate a raw Fernet key (base64, urlsafe 32 bytes)."""
    return Fernet.generate_key()

def encrypt_dek_with_mek(dek: bytes) -> bytes:
    """Encrypt DEK with MEK for storage on the user record."""
    return MEK.encrypt(dek)

def decrypt_dek_with_mek(dek_encrypted: bytes) -> bytes:
    return MEK.decrypt(dek_encrypted)

def fernet_for_user(dek_encrypted: bytes) -> Fernet:
    dek = decrypt_dek_with_mek(dek_encrypted)
    return Fernet(dek)

def encrypt_secret_for_user(plaintext: str, dek_encrypted: bytes) -> bytes:
    f = fernet_for_user(dek_encrypted)
    return f.encrypt(plaintext.encode())

def decrypt_secret_for_user(ciphertext: bytes, dek_encrypted: bytes) -> str:
    f = fernet_for_user(dek_encrypted)
    return f.decrypt(ciphertext).decode()