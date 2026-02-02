from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.modules.persons.service import get_all_persons, create_person

router = APIRouter(prefix="/persons", tags=["Persons"])

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def persons_page(request: Request, db: Session = Depends(get_db)):
    persons = get_all_persons(db)
    return templates.TemplateResponse(
        "persons.html",
        {
            "request": request,
            "persons": persons
        }
    )


@router.post("/create")
def add_person(
    name: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    create_person(db, name, category)
    return RedirectResponse("/persons", status_code=303)
