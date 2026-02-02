from fastapi import APIRouter, Depends, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pandas as pd

from app.database.database import SessionLocal
from app.modules.journal.service import import_journal_from_excel

router = APIRouter(prefix="/journal", tags=["Journal"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/import", response_class=HTMLResponse)
def import_page(request: Request):
    return templates.TemplateResponse(
        "journal_import.html",
        {"request": request}
    )


@router.post("/import")
async def import_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    df = pd.read_excel(file.file, sheet_name="JOURNAL_RAW")

    # تنظيف وترتيب الأعمدة
    df.columns = [
        "EntryNo",
        "Date",
        "Currency",
        "Description",
        "Account",
        "Debit",
        "Credit",
        "PersonTag",
        "TypeTag",
    ]

    df = df.fillna("")

    rows = df.to_dict(orient="records")

    import_journal_from_excel(db, rows)

    return RedirectResponse("/journal", status_code=303)
