from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Currency
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/currencies", tags=["API Currencies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_currencies(token: str = Header(...), db: Session = Depends(get_db)):
    get_current_user(token)
    return db.query(Currency).all()
