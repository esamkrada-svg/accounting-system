from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from app.database.database import SessionLocal
from app.modules.reports.service import (
    get_trial_balance_data,
    get_account_statement_data,
    get_person_statement_data
)

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
