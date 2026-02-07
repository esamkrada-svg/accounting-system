from sqlalchemy.orm import Session
from app.database.models import User
import hashlib


def hash_password(password: str) -> str:
    # توحيد الطول لتفادي أي مشاكل مستقبلية
    password = password.strip()
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(db: Session, username: str, password: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None

        hashed = hash_password(password)
        if user.password_hash != hashed:
            return None

        return user

    except Exception as e:
        # نطبع الخطأ في Logs بدل إسقاط التطبيق
        print("AUTH ERROR:", e)
        return None
