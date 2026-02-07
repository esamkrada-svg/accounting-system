from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import AccountingPeriod, JournalEntry, Account
from app.modules.opening.service import create_opening_entry

router = APIRouter(prefix="/opening", tags=["Opening"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================
# 🟢 صفحة القيد الافتتاحي
# ===============================
@router.get("/", response_class=HTMLResponse)
def opening_entry_page(request: Request, db: Session = Depends(get_db)):
    # 1️⃣ التأكد من وجود فترة محاسبية مفتوحة
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

    # 3️⃣ جلب الحسابات
    accounts = db.query(Account).order_by(Account.code).all()

    return templates.TemplateResponse(
        "opening/index.html",
        {
            "request": request,
            "period": period,
            "accounts": accounts
        }
    )


# ===============================
# 💾 حفظ القيد الافتتاحي
# ===============================
@router.post("/create")
async def create_opening(request: Request, db: Session = Depends(get_db)):
    form = dict(await request.form())

    rows = []

    for key, value in form.items():
        if not value:
            continue

        if key.startswith("debit_") or key.startswith("credit_"):
            _, acc_id = key.split("_")
            acc_id = int(acc_id)

            row = next((r for r in rows if r["account_id"] == acc_id), None)
            if not row:
                row = {"account_id": acc_id, "debit": 0, "credit": 0}
                rows.append(row)

            if key.startswith("debit_"):
                row["debit"] = float(value)
            else:
                row["credit"] = float(value)

    create_opening_entry(db, rows)

    return RedirectResponse("/opening", status_code=303)
