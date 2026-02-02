from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Account, Person, Currency
from app.modules.journal.service import create_journal_entry, get_all_entries

router = APIRouter(prefix="/journal", tags=["Journal"])

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def journal_page(request: Request, db: Session = Depends(get_db)):
    entries = get_all_entries(db)
    accounts = db.query(Account).all()
    persons = db.query(Person).all()
    currencies = db.query(Currency).all()

    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "entries": entries,
            "accounts": accounts,
            "persons": persons,
            "currencies": currencies,
        }
    )


@router.post("/create")
def create_entry(
    entry_no: int = Form(...),
    date: str = Form(...),
    description: str = Form(...),
    currency_id: int = Form(...),
    account_id: int = Form(...),
    debit: float = Form(0),
    credit: float = Form(0),
    person_id: int = Form(None),
    db: Session = Depends(get_db)
):
    lines = [{
        "account_id": account_id,
        "debit": debit,
        "credit": credit,
        "person_id": person_id
    }]

    create_journal_entry(
        db=db,
        entry_no=entry_no,
        date=date,
        description=description,
        currency_id=currency_id,
        lines=lines
    )

    return RedirectResponse("/journal", status_code=303)
