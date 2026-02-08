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

    # 2️⃣ إذا القيد الافتتاحي موجود مسبقًا -> ممنوع
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

    # 3️⃣ ممنوع إنشاء افتتاحي إذا توجد أي قيود أخرى بالفعل
    any_existing_entry = (
        db.query(JournalEntry)
        .filter(JournalEntry.description != "Opening Balance")
        .first()
    )
    if any_existing_entry:
        return templates.TemplateResponse(
            "opening/message.html",
            {
                "request": request,
                "message": "❌ يوجد قيود محاسبية سابقة بالفعل. لا يمكن إنشاء القيد الافتتاحي بعد وجود قيود. احذف القيود التجريبية/صفّر قاعدة البيانات ثم أعد المحاولة."
            }
        )

    # 4️⃣ جلب الحسابات
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

    # حماية إضافية: إذا الافتتاحي موجود -> ممنوع
    opening_exists = (
        db.query(JournalEntry)
        .filter(JournalEntry.description == "Opening Balance")
        .first()
    )
    if opening_exists:
        return RedirectResponse("/opening", status_code=303)

    # حماية إضافية: إذا توجد أي قيود أخرى -> ممنوع
    any_existing_entry = (
        db.query(JournalEntry)
        .filter(JournalEntry.description != "Opening Balance")
        .first()
    )
    if any_existing_entry:
        return templates.TemplateResponse(
            "opening/message.html",
            {
                "request": request,
                "message": "❌ لا يمكن حفظ القيد الافتتاحي لأن هناك قيودًا سابقة. احذف القيود التجريبية/صفّر قاعدة البيانات ثم أعد المحاولة."
            }
        )

    form = dict(await request.form())
    rows = []

    # form keys مثل debit_1100 / credit_3100
    for key, value in form.items():
        if value is None or str(value).strip() == "":
            continue

        if key.startswith("debit_") or key.startswith("credit_"):
            _, acc_id = key.split("_")
            acc_id = int(acc_id)

            row = next((r for r in rows if r["account_id"] == acc_id), None)
            if not row:
                row = {"account_id": acc_id, "debit": 0.0, "credit": 0.0}
                rows.append(row)

            if key.startswith("debit_"):
                row["debit"] = float(value)
            else:
                row["credit"] = float(value)

    try:
        # Service تقوم بإنشاء القيد الافتتاحي
        create_opening_entry(db, rows)

        # ✅ تثبيت الحالة النهائية: لازم يكون posted=True دائمًا
        opening = (
            db.query(JournalEntry)
            .filter(JournalEntry.description == "Opening Balance")
            .first()
        )
        if opening:
            opening.posted = True
            # يفضل أن يبقى entry_no فارغ/None أو 0 — اخترنا 0 كتمييز افتتاحي
            if opening.entry_no is None:
                opening.entry_no = 0
            db.commit()

    except Exception as e:
        db.rollback()
        return templates.TemplateResponse(
            "opening/message.html",
            {
                "request": request,
                "message": f"❌ فشل إنشاء القيد الافتتاحي: {str(e)}"
            }
        )

    return templates.TemplateResponse(
        "opening/message.html",
        {
            "request": request,
            "message": "✅ تم إنشاء القيد الافتتاحي بنجاح. يمكنك الآن البدء باستخدام النظام."
        }
    )
