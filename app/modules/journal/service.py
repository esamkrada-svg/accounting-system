from sqlalchemy.orm import Session
from app.database.models import JournalEntry, JournalLine, AccountingPeriod
from datetime import date


def is_date_closed(db: Session, entry_date: date) -> bool:
    period = (
        db.query(AccountingPeriod)
        .filter(AccountingPeriod.start_date <= entry_date)
        .filter(AccountingPeriod.end_date >= entry_date)
        .filter(AccountingPeriod.closed == True)
        .first()
    )
    return period is not None


def create_journal_entry(
    db: Session,
    entry_no: int,
    date,
    description: str,
    currency_id: int,
    lines: list
):
    if is_date_closed(db, date):
        raise ValueError("Accounting period is closed")

    total_debit = sum(l["debit"] for l in lines)
    total_credit = sum(l["credit"] for l in lines)

    if round(total_debit, 2) != round(total_credit, 2):
        raise ValueError("Debit and Credit not balanced")

    entry = JournalEntry(
        entry_no=entry_no,
        date=date,
        description=description,
        currency_id=currency_id,
        posted=False
    )
    db.add(entry)
    db.flush()

    for line in lines:
        db.add(
            JournalLine(
                entry_id=entry.id,
                account_id=line["account_id"],
                debit=line["debit"],
                credit=line["credit"],
                person_id=line.get("person_id")
            )
        )

    db.commit()
    return entry
