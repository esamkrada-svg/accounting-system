import os
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, User

# ✅ استخدام DATABASE_URL من Railway
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ✅ إنشاء admin مرة واحدة فقط
        exists = db.query(User).filter(User.username == "admin").first()
        if not exists:
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
