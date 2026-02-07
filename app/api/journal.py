from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import JournalEntry
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/journal", tags=["API Journal"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_entries(token: str = Header(...), db: Session = Depends(get_db)):
    get_current_user(token)
    return db.query(JournalEntry).all()
