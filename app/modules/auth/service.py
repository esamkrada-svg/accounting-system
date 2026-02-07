from sqlalchemy.orm import Session
from app.database.models import User
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    if user.password_hash != hash_password(password):
        return None

    return user
