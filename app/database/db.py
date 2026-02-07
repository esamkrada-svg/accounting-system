# ================= BCRYPT HARD FIX =================
import os
os.environ["PASSLIB_BCRYPT_NOCHECK"] = "1"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.database.models import Base, User

# ================= DATABASE =================
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

# ================= PASSWORD =================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def _safe_password(password: str) -> str:
    # bcrypt supports ONLY 72 bytes
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    return pwd_context.hash(_safe_password(password))

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(_safe_password(password), hashed)

# ================= INIT DB =================
def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin created (admin / admin123)")
    finally:
        db.close()
