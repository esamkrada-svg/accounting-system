from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, User
import hashlib

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    # إنشاء الجداول
    Base.metadata.create_all(bind=engine)

    # إنشاء مستخدم admin افتراضي
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()

        if not admin:
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin",
            )
            db.add(admin)
            db.commit()
            print("✅ Default admin user created (admin / admin123)")
        else:
            print("ℹ️ Admin user already exists")

    finally:
        db.close()
