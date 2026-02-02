from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.modules.accounts.service import get_all_accounts, create_account

router = APIRouter(prefix="/accounts", tags=["Accounts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def accounts_page(request: Request, db: Session = Depends(get_db)):
    accounts = get_all_accounts(db)
    return {
        "accounts": accounts,
        "request": request
    }


@router.post("/create")
def add_account(
    code: str = Form(...),
    name: str = Form(...),
    type: str = Form(...),
    db: Session = Depends(get_db)
):
    create_account(db, code, name, type)
    return RedirectResponse("/accounts", status_code=303)
