from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, User
import hashlib

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


def hash_password(password: str) -> str:
    password = password.strip()
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    # إنشاء الجداول
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # حذف admin القديم إن وجد
        db.query(User).filter(User.username == "admin").delete()
        db.commit()

        # إنشاء admin جديد
        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
            role="admin"
        )
        db.add(admin)
        db.commit()

        print("✅ Admin READY (admin / admin123)")

    finally:
        db.close()
