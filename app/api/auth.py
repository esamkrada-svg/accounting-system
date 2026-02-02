from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import secrets

from app.database.database import SessionLocal
from app.database.models import User
from passlib.hash import bcrypt

router = APIRouter(prefix="/api/auth", tags=["API Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    role: str


tokens = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_hex(16)
    tokens[token] = user
    return {"token": token, "role": user.role}


def get_current_user(token: str):
    user = tokens.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
