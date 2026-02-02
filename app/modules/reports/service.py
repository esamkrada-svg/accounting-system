from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import JournalLine, JournalEntry, Account, Person


def get_trial_balance_data(db: Session):
    return (
        db.query(
            Account.code.label("Code"),
            Account.name.label("Account"),
            func.sum(JournalLine.debit).label("Debit"),
            func.sum(JournalLine.credit).label("Credit"),
        )
        .join(JournalLine, Account.id == JournalLine.account_id)
        .join(JournalEntry, JournalEntry.id == JournalLine.entry_id)
        .filter(JournalEntry.posted == True)
        .group_by(Account.id)
        .order_by(Account.code)
        .all()
    )


def get_account_statement_data(db: Session, account_id: int):
    return (
        db.query(
            JournalEntry.date,
            JournalEntry.entry_no,
            JournalEntry.description,
            JournalLine.debit,
            JournalLine.credit,
        )
        .join(JournalLine, JournalEntry.id == JournalLine.entry_id)
        .filter(JournalLine.account_id == account_id)
        .filter(JournalEntry.posted == True)
        .order_by(JournalEntry.date)
        .all()
    )


def get_person_statement_data(db: Session, person_id: int):
    return (
        db.query(
            JournalEntry.date,
            JournalEntry.entry_no,
            JournalEntry.description,
            JournalLine.debit,
            JournalLine.credit,
        )
        .join(JournalLine, JournalEntry.id == JournalLine.entry_id)
        .filter(JournalLine.person_id == person_id)
        .filter(JournalEntry.posted == True)
        .order_by(JournalEntry.date)
        .all()
    )
