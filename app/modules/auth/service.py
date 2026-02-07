from sqlalchemy.orm import Session
from app.database.models import User
from app.database.db import verify_password


def authenticate(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
