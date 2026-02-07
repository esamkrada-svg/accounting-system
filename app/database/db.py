from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
import os

from app.database.models import Base, User

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ================= PASSWORD (STABLE) =================

_SALT = "ACCOUNTING_SYSTEM_SALT"

def hash_password(password: str) -> str:
    raw = f"{_SALT}:{password}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# ================= INIT DB =================

def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("✅ Admin created: admin / admin123")
    finally:
        db.close()
