from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pandas as pd
import io

from app.database.db import SessionLocal
from app.modules.reports.service import (
    get_trial_balance_data,
    get_account_statement_data,
    get_person_statement_data
)

router = APIRouter(prefix="/reports", tags=["Reports"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 📊 Reports Index (HTML)
# =========================
@router.get("/", response_class=HTMLResponse)
def reports_index(request: Request):
    return templates.TemplateResponse(
        "reports/index.html",
        {"request": request}
    )


# =========================
# 🧾 Trial Balance (HTML)
# =========================
@router.get("/trial-balance", response_class=HTMLResponse)
def trial_balance_page(request: Request, db: Session = Depends(get_db)):
    rows = get_trial_balance_data(db)

    trial_balance = []
    for r in rows:
        debit = r.Debit or 0
        credit = r.Credit or 0

        balance = debit - credit
        balance_type = "مدين" if balance > 0 else "دائن" if balance < 0 else ""

        trial_balance.append({
            "code": r.Code,
            "name": r.Account,
            "debit": debit,
            "credit": credit,
            "balance": abs(balance),
            "balance_type": balance_type
        })

    return templates.TemplateResponse(
        "reports/trial_balance.html",
        {
            "request": request,
            "rows": trial_balance
        }
    )


# =========================
# 📥 Export Trial Balance
# =========================
@router.get("/export/trial-balance")
def export_trial_balance(db: Session = Depends(get_db)):
    data = get_trial_balance_data(db)
    df = pd.DataFrame(data)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Trial Balance")

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=trial_balance.xlsx"}
    )


# =========================
# 📥 Export Account Statement
# =========================
@router.get("/export/account/{account_id}")
def export_account_statement(account_id: int, db: Session = Depends(get_db)):
    data = get_account_statement_data(db, account_id)
    df = pd.DataFrame(data)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Account Statement")

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=account_statement.xlsx"}
    )


# =========================
# 📥 Export Person Statement
# =========================
@router.get("/export/person/{person_id}")
def export_person_statement(person_id: int, db: Session = Depends(get_db)):
    data = get_person_statement_data(db, person_id)
    df = pd.DataFrame(data)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Person Statement")

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=person_statement.xlsx"}
    )
