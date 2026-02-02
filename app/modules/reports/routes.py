from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Account, Person
from app.modules.reports.service import (
    account_statement,
    person_statement,
    trial_balance
)

router = APIRouter(prefix="/reports", tags=["Reports"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def reports_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "accounts": db.query(Account).all(),
            "persons": db.query(Person).all(),
            "trial_balance": trial_balance(db),
        }
    )


@router.post("/account", response_class=HTMLResponse)
def report_account(
    request: Request,
    account_id: int = Form(...),
    db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "accounts": db.query(Account).all(),
            "persons": db.query(Person).all(),
            "account_report": account_statement(db, account_id),
        }
    )


@router.post("/person", response_class=HTMLResponse)
def report_person(
    request: Request,
    person_id: int = Form(...),
    db: Session = Depends(get_db)
):
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "accounts": db.query(Account).all(),
            "persons": db.query(Person).all(),
            "person_report": person_statement(db, person_id),
        }
    )
