from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Account, Person, Currency, JournalEntry
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
    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "entries": get_all_entries(db),
            "accounts": db.query(Account).all(),
            "persons": db.query(Person).all(),
            "currencies": db.query(Currency).all(),
        }
    )


@router.post("/create")
def create_entry(
    entry_no: int = Form(...),
    date: str = Form(...),
    description: str = Form(...),
    currency_id: int = Form(...),
    account_id: list[int] = Form(...),
    debit: list[float] = Form(...),
    credit: list[float] = Form(...),
    person_id: list[int] = Form([]),
    db: Session = Depends(get_db)
):
    lines = []

    for i in range(len(account_id)):
        lines.append({
            "account_id": account_id[i],
            "debit": debit[i] or 0,
            "credit": credit[i] or 0,
            "person_id": person_id[i] if i < len(person_id) else None
        })

    create_journal_entry(
        db=db,
        entry_no=entry_no,
        date=date,
        description=description,
        currency_id=currency_id,
        lines=lines
    )

    return RedirectResponse("/journal", status_code=303)


@router.post("/post/{entry_id}")
def post_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).get(entry_id)

    if entry and not entry.posted:
        entry.posted = True
        db.commit()

    return RedirectResponse("/journal", status_code=303)
