from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.modules.currencies.service import (
    get_all_currencies,
    create_currency,
    toggle_currency
)

router = APIRouter(prefix="/currencies", tags=["Currencies"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def currencies_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "currencies.html",
        {
            "request": request,
            "currencies": get_all_currencies(db)
        }
    )


@router.post("/create")
def add_currency(
    code: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    create_currency(db, code, name)
    return RedirectResponse("/currencies", status_code=303)


@router.post("/toggle/{currency_id}")
def toggle(currency_id: int, db: Session = Depends(get_db)):
    toggle_currency(db, currency_id)
    return RedirectResponse("/currencies", status_code=303)
