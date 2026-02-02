from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from app.database.database import SessionLocal
from app.database.models import Currency
from app.modules.exchange_rates.service import get_rates, add_rate

router = APIRouter(prefix="/exchange-rates", tags=["Exchange Rates"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def rates_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "exchange_rates.html",
        {
            "request": request,
            "rates": get_rates(db),
            "currencies": db.query(Currency).filter(Currency.active == True).all()
        }
    )


@router.post("/create")
def create_rate(
    currency_id: int = Form(...),
    rate: float = Form(...),
    effective_date: date = Form(...),
    db: Session = Depends(get_db)
):
    add_rate(db, currency_id, rate, effective_date)
    return RedirectResponse("/exchange-rates", status_code=303)
