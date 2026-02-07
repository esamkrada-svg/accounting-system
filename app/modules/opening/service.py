from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database.models import (
    JournalEntry,
    JournalLine,
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

    # 🔹 تأكد أنه لا يوجد افتتاحي سابق
    opening_exists = (
        db.query(JournalEntry)
        .filter(JournalEntry.description == "Opening Balance")
        .first()
    )
    if opening_exists:
        raise ValueError("✅ القيد الافتتاحي موجود مسبقًا ولا يمكن إنشاؤه مرة أخرى")

    # 🔹 منع أي قيود قبل الافتتاحي
    any_other_entries = (
        db.query(JournalEntry)
        .filter(JournalEntry.description != "Opening Balance")
        .first()
    )
    if any_other_entries:
        raise ValueError("❌ يوجد قيود سابقة. لا يمكن إنشاء افتتاحي بعد وجود قيود")

    # 🔹 رقم القيد: ليس 1 ثابت (حتى لا يصطدم)
    # نبدأ من 1 فعلاً، لكن نحسبه ديناميك
    max_no = db.query(func.max(JournalEntry.entry_no)).scalar()
    next_no = (max_no or 0) + 1

    # 🔹 إنشاء القيد الافتتاحي (مرحّل)
    entry = JournalEntry(
        entry_no=next_no,
        date=date.today(),
        description="Opening Balance",
        currency_id=base_currency.id,
        posted=True
    )
    db.add(entry)
    db.flush()

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
        db.rollback()
        raise ValueError("❌ القيد الافتتاحي غير متوازن")

    db.commit()
