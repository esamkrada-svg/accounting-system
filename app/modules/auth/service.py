from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.database.models import User


def create_user(db: Session, username: str, password: str, role: str):
    user = User(
        username=username,
        password_hash=bcrypt.hash(password),
        role=role
    )
    db.add(user)
    db.commit()
    return user


def authenticate(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.verify(password, user.password_hash):
        return user
    return None
