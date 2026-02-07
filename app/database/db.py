from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, User
from passlib.context import CryptContext
import os

# ================= DATABASE =================
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ================= PASSWORD CONTEXT =================
# تعطيل bcrypt wrap bug (مهم مع Python 3.13)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",          # تثبيت ident
    bcrypt__rounds=12,
)

# تعطيل فحص wrap bug صراحة
os.environ["PASSLIB_BCRYPT_NOCHECK"] = "1"


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def init_db():
    # 1. إنشاء الجداول
    Base.metadata.create_all(bind=engine)

    # 2. إنشاء مستخدم admin افتراضي
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("✅ Default admin user created (admin / admin123)")
        else:
            print("ℹ️ Admin user already exists")
    finally:
        db.close()
