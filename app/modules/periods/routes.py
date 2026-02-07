from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from app.database.db import SessionLocal
from app.database.models import AccountingPeriod

router = APIRouter(prefix="/periods", tags=["Periods"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def periods_page(request: Request, db: Session = Depends(get_db)):
    periods = db.query(AccountingPeriod).order_by(AccountingPeriod.start_date).all()
    return templates.TemplateResponse(
        "periods.html",
        {"request": request, "periods": periods}
    )


@router.post("/create")
def create_period(
    start_date: date = Form(...),
    end_date: date = Form(...),
    db: Session = Depends(get_db)
):
    db.add(AccountingPeriod(start_date=start_date, end_date=end_date))
    db.commit()
    return RedirectResponse("/periods", status_code=303)


@router.post("/toggle/{period_id}")
def toggle_period(period_id: int, db: Session = Depends(get_db)):
    period = db.query(AccountingPeriod).get(period_id)
    if period:
        period.closed = not period.closed
        db.commit()
    return RedirectResponse("/periods", status_code=303)
