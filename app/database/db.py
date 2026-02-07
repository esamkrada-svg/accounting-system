# ================= PASSLIB FIX (MUST BE FIRST) =================
import os
os.environ["PASSLIB_BCRYPT_NOCHECK"] = "1"

# ================= IMPORTS =================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.database.models import Base, User

# ================= DATABASE CONFIG =================
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

# ================= PASSWORD CONTEXT =================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__ident="2b",
    bcrypt__rounds=12,
)

# ================= DB INIT =================
def init_db():
    """
    - Create all tables
    - Create default admin user if not exists
    """
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        admin = db.query(User).filter(User.username == "admin").first()

        if not admin:
            admin_user = User(
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created (admin / admin123)")
        else:
            print("ℹ️ Admin user already exists")

    finally:
        db.close()
