from sqlalchemy.orm import Session
from app.database.models import JournalEntry, JournalLine


def create_journal_entry(
    db: Session,
    entry_no: int,
    date,
    description: str,
    currency_id: int,
    lines: list
):
    entry = JournalEntry(
        entry_no=entry_no,
        date=date,
        description=description,
        currency_id=currency_id,
        posted=False
    )
    db.add(entry)
    db.flush()  # للحصول على entry.id

    for line in lines:
        jl = JournalLine(
            entry_id=entry.id,
            account_id=line.account_id,
            debit=line.debit,
            credit=line.credit,
            person_id=line.person_id
        )
        db.add(jl)

    db.commit()
    db.refresh(entry)
    return entry


def get_all_entries(db: Session):
    return db.query(JournalEntry).order_by(JournalEntry.entry_no.desc()).all()
