from sqlalchemy.orm import Session
from datetime import date

from app.database.models import (
    JournalEntry,
    JournalLine,
    Account,
    Currency
)


def create_opening_entry(db: Session, rows: list):
    # 🔹 جلب العملة الأساسية
    base_currency = (
        db.query(Currency)
        .filter(Currency.is_base == True)
        .first()
    )

    if not base_currency:
        raise ValueError("❌ لا توجد عملة أساسية معرفة في النظام")

    # 🔹 إنشاء القيد الافتتاحي (مرحّل)
    entry = JournalEntry(
        entry_no=1,
        date=date.today(),
        description="Opening Balance",
        currency_id=base_currency.id,
        posted=True
    )
    db.add(entry)
    db.flush()  # للحصول على entry.id

    total_debit = 0.0
    total_credit = 0.0

    for r in rows:
        debit = float(r.get("debit") or 0)
        credit = float(r.get("credit") or 0)

        if debit == 0 and credit == 0:
            continue

        line = JournalLine(
            entry_id=entry.id,
            account_id=r["account_id"],
            debit=debit,
            credit=credit
        )
        db.add(line)

        total_debit += debit
        total_credit += credit

    # 🔹 التحقق من التوازن
    if round(total_debit, 2) != round(total_credit, 2):
        raise ValueError("❌ القيد الافتتاحي غير متوازن")

    db.commit()
