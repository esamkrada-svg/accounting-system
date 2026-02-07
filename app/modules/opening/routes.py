from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import (
    AccountingPeriod,
    JournalEntry,
    Account
)
from app.modules.opening.service import create_opening_entry

router = APIRouter(prefix="/opening", tags=["Opening"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def opening_entry_page(request: Request, db: Session = Depends(get_db)):
    period = (
        db.query(AccountingPeriod)
        .filter(AccountingPeriod.closed == False)
        .order_by(AccountingPeriod.start_date)
        .first()
    )

    if not period:
        return templates.TemplateResponse(
            "opening/message.html",
            {
                "request": request,
                "message": "❌ لا توجد فترة محاسبية مفتوحة."
            }
        )

    opening_exists = (
        db.query(JournalEntry)
        .filter(JournalEntry.description == "Opening Balance")
        .first()
    )

    if opening_exists:
        return templates.TemplateResponse(
            "opening/message.html",
            {
                "request": request,
                "message": "✅ القيد الافتتاحي موجود ولا يمكن تعديله."
            }
        )

    accounts = db.query(Account).order_by(Account.code).all()

    return templates.TemplateResponse(
        "opening/index.html",
        {
            "request": request,
            "period": period,
            "accounts": accounts
        }
    )


@router.post("/create")
def create_opening(request: Request, db: Session = Depends(get_db)):
    form = dict(await request.form())

    rows = []
    for key, value in form.items():
        if key.startswith("debit_") or key.startswith("credit_"):
            _, acc_id = key.split("_")
            acc_id = int(acc_id)

            row = next((r for r in rows if r["account_id"] == acc_id), None)
            if not row:
                row = {"account_id": acc_id, "debit": 0, "credit": 0}
                rows.append(row)

            if key.startswith("debit_"):
                row["debit"] = value
            else:
                row["credit"] = value

    create_opening_entry(db, rows)

    return RedirectResponse("/opening/posted", status_code=303)


@router.get("/posted", response_class=HTMLResponse)
def opening_saved(request: Request):
    return templates.TemplateResponse(
        "opening/message.html",
        {
            "request": request,
            "message": "✅ تم حفظ القيد الافتتاحي بنجاح. يرجى ترحيله للمتابعة."
        }
    )
