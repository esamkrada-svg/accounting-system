from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.db import SessionLocal
from app.database.models import Account, JournalLine, JournalEntry
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["API Reports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/trial-balance")
def trial_balance(token: str = Header(...), db: Session = Depends(get_db)):
    get_current_user(token)
    return (
        db.query(
            Account.code,
            Account.name,
            func.sum(JournalLine.debit),
            func.sum(JournalLine.credit)
        )
        .join(JournalLine, Account.id == JournalLine.account_id)
        .join(JournalEntry, JournalEntry.id == JournalLine.entry_id)
        .filter(JournalEntry.posted == True)
        .group_by(Account.id)
        .all()
    )
