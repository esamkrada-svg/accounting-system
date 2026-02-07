from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_default_admin(db: Session):
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        return

    password_hash = pwd_context.hash("admin123")

    admin = User(
        username="admin",
        password_hash=password_hash,
        role="admin"
    )

    db.add(admin)
    db.commit()
