from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import (
    AccountingPeriod,
    JournalEntry
)

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
    # 1️⃣ التأكد من وجود فترة مفتوحة
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
                "message": "❌ لا توجد فترة محاسبية مفتوحة. الرجاء إنشاء فترة أولًا."
            }
        )

    # 2️⃣ التأكد من عدم وجود قيد افتتاحي سابق
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
                "message": "✅ القيد الافتتاحي تم إنشاؤه مسبقًا ولا يمكن تعديله."
            }
        )

    # 3️⃣ السماح بالانتقال لشاشة الإدخال (لاحقًا)
    return templates.TemplateResponse(
        "opening/index.html",
        {
            "request": request,
            "period": period
        }
    )
