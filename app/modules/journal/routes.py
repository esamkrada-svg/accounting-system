from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from app.database.db import SessionLocal
from app.database.models import JournalEntry, JournalLine, Account

router = APIRouter(prefix="/journal", tags=["Journal"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 📄 قائمة القيود اليومية
# =========================
@router.get("/", response_class=HTMLResponse)
def journal_index(request: Request, db: Session = Depends(get_db)):
    entries = db.query(JournalEntry).order_by(JournalEntry.date.desc()).all()

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
    accounts = db.query(Account).order_by(Account.code).all()

    return templates.TemplateResponse(
        "journal/create.html",
        {
            "request": request,
            "accounts": accounts
        }
    )


# =========================
# 💾 حفظ القيد اليومي
# =========================
@router.post("/create")
async def save_journal_entry(
    request: Request,
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    form = await request.form()

    entry = JournalEntry(
        date=date.today(),
        description=description,
        posted=False
    )
    db.add(entry)
    db.flush()

    total_debit = 0
    total_credit = 0

    accounts = db.query(Account).all()

    for acc in accounts:
        debit = float(form.get(f"debit_{acc.id}") or 0)
        credit = float(form.get(f"credit_{acc.id}") or 0)

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
        return HTMLResponse("❌ القيد غير متوازن (المدين ≠ الدائن)", status_code=400)

    db.commit()
    return RedirectResponse("/journal", status_code=303)
