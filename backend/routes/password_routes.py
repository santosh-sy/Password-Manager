from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_current_user
from backend.database import get_db
from backend.models import VaultItem, User
from backend.schemas import VaultItemCreate, VaultItemOut
from backend.utils.crypto_utils import encrypt_secret_for_user, decrypt_secret_for_user

router = APIRouter()

@router.post("", response_model=VaultItemOut)
def create_item(body: VaultItemCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ciphertext = encrypt_secret_for_user(body.secret, user.dek_encrypted)
    item = VaultItem(user_id=user.id, name=body.name, username=body.username, secret_ciphertext=ciphertext)
    db.add(item)
    db.commit()
    db.refresh(item)
    return VaultItemOut(id=item.id, name=item.name, username=item.username)

@router.get("", response_model=list[VaultItemOut])
def list_items(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(VaultItem).filter(VaultItem.user_id == user.id).all()
    return [VaultItemOut(id=i.id, name=i.name, username=i.username) for i in items]

@router.get("/{item_id}/secret")
def get_item_secret(item_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(VaultItem).filter(VaultItem.id == item_id, VaultItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    secret = decrypt_secret_for_user(item.secret_ciphertext, user.dek_encrypted)
    return {"id": item.id, "name": item.name, "username": item.username, "secret": secret}
