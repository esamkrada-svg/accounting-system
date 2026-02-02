from sqlalchemy.orm import Session
from app.database.models import (
    JournalEntry,
    JournalLine,
    Account,
    Person,
    Currency
)
from datetime import date


def import_journal_from_excel(db: Session, rows: list[dict]):
    entries = {}

    for r in rows:
        entry_no = int(r["EntryNo"])

        if entry_no not in entries:
            # إنشاء أو جلب العملة
            currency = (
                db.query(Currency)
                .filter(Currency.code == r["Currency"])
                .first()
            )
            if not currency:
                currency = Currency(code=r["Currency"], name=r["Currency"])
                db.add(currency)
                db.flush()

            entry_date = r["Date"] or date.today()

            entry = JournalEntry(
                entry_no=entry_no,
                date=entry_date,
                description=r["Description"],
                currency_id=currency.id,
                posted=False
            )
            db.add(entry)
            db.flush()

            entries[entry_no] = entry

        # الحساب
        account = (
            db.query(Account)
            .filter(Account.code == r["Account"])
            .first()
        )
        if not account:
            account = Account(
                code=r["Account"],
                name=r["Account"],
                type="Expense"
            )
            db.add(account)
            db.flush()

        # الشخص (اختياري)
        person = None
        if r.get("PersonTag"):
            person = (
                db.query(Person)
                .filter(Person.name == r["PersonTag"])
                .first()
            )
            if not person:
                person = Person(
                    name=r["PersonTag"],
                    category="other"
                )
                db.add(person)
                db.flush()

        line = JournalLine(
            entry_id=entries[entry_no].id,
            account_id=account.id,
            debit=float(r["Debit"] or 0),
            credit=float(r["Credit"] or 0),
            person_id=person.id if person else None
        )
        db.add(line)

    db.commit()
