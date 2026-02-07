from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.database.db import SessionLocal
from app.database.models import (
    JournalEntry,
    JournalLine,
    Account,
    AccountingPeriod
)

router = APIRouter(prefix="/journal", tags=["Journal"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# ✅ قواعد أساسية
# =========================
def ensure_open_period(db: Session):
    """لا يسمح بأي عملية ترحيل إلا بوجود فترة مفتوحة."""
    period = (
        db.query(AccountingPeriod)
        .filter(AccountingPeriod.closed == False)
        .order_by(AccountingPeriod.start_date)
        .first()
    )
    if not period:
        raise ValueError("❌ لا توجد فترة محاسبية مفتوحة. الرجاء إنشاء/فتح فترة أولاً.")


def ensure_opening_exists(db: Session):
    """لا يسمح بعمل قيود/ترحيل قبل القيد الافتتاحي."""
    opening = (
        db.query(JournalEntry)
        .filter(JournalEntry.description == "Opening Balance", JournalEntry.posted == True)
        .first()
    )
    if not opening:
        raise ValueError("❌ لا يمكن إنشاء/ترحيل قيود قبل إنشاء القيد الافتتاحي (Opening Balance).")


# =========================
# 📄 قائمة القيود اليومية
# =========================
@router.get("/", response_class=HTMLResponse)
def journal_index(request: Request, db: Session = Depends(get_db)):
    entries = db.query(JournalEntry).order_by(JournalEntry.id.desc()).all()

    return templates.TemplateResponse(
        "journal/index.html",
        {
            "request": request,
            "entries": entries
        }
    )


# =========================
# ➕ شاشة إنشاء قيد جديد
# =========================
@router.get("/create", response_class=HTMLResponse)
def create_journal_page(request: Request, db: Session = Depends(get_db)):
    # ✅ القاعدة: لا قيود قبل الافتتاحي
    try:
        ensure_opening_exists(db)
    except Exception as e:
        return HTMLResponse(str(e), status_code=400)

    accounts = db.query(Account).order_by(Account.code).all()

    return templates.TemplateResponse(
        "journal/create.html",
        {
            "request": request,
            "accounts": accounts
        }
    )


# =========================
# 💾 حفظ القيد اليومي (غير مرحّل)
# =========================
@router.post("/create")
async def save_journal_entry(
    request: Request,
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    # ✅ القاعدة: لا قيود قبل الافتتاحي
    try:
        ensure_opening_exists(db)
    except Exception as e:
        return HTMLResponse(str(e), status_code=400)

    entry = JournalEntry(
        date=date.today(),
        description=description,
        posted=False,
        entry_no=None  # طبيعي يظل None إلى وقت الترحيل
    )
    db.add(entry)
    db.flush()

    form = await request.form()

    total_debit = 0.0
    total_credit = 0.0

    accounts = db.query(Account).all()

    for acc in accounts:
        debit = float(form.get(f"debit_{acc.id}", 0) or 0)
        credit = float(form.get(f"credit_{acc.id}", 0) or 0)

        if debit == 0 and credit == 0:
            continue

        line = JournalLine(
            entry_id=entry.id,
            account_id=acc.id,
            debit=debit,
            credit=credit
        )
        db.add(line)

        total_debit += debit
        total_credit += credit

    if round(total_debit, 2) != round(total_credit, 2):
        db.rollback()
        return HTMLResponse("❌ القيد غير متوازن", status_code=400)

    db.commit()
    return RedirectResponse("/journal", status_code=303)


# =========================
# ✅ ترحيل القيد
# =========================
@router.post("/post/{entry_id}")
def post_journal_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()

    if not entry:
        return HTMLResponse("❌ القيد غير موجود", status_code=404)

    if entry.posted:
        return RedirectResponse("/journal", status_code=303)

    # ✅ القاعدة: لا ترحيل بدون فترة مفتوحة
    try:
        ensure_open_period(db)
    except Exception as e:
        return HTMLResponse(str(e), status_code=400)

    # ✅ القاعدة: لا ترحيل قبل الافتتاحي
    try:
        ensure_opening_exists(db)
    except Exception as e:
        return HTMLResponse(str(e), status_code=400)

    # توليد رقم قيد تلقائي (تسلسلي)
    max_no = db.query(func.max(JournalEntry.entry_no)).scalar() or 0
    entry.entry_no = max_no + 1
    entry.posted = True

    db.commit()
    return RedirectResponse("/journal", status_code=303)
