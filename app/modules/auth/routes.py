from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# ✅ المصدر الصحيح والوحيد
from app.database.db import SessionLocal
from app.database.models import Account

router = APIRouter(tags=["Accounts"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/accounts", response_class=HTMLResponse)
def list_accounts(request: Request, db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return templates.TemplateResponse(
        "accounts.html",
        {"request": request, "accounts": accounts}
    )
