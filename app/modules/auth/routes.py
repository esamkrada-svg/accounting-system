from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.modules.auth.service import authenticate

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None}
    )


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = authenticate(db, username, password)

    if not user:
        # ❗ بدل 500 → رسالة واضحة
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "اسم المستخدم أو كلمة المرور غير صحيحة",
            },
            status_code=401,
        )

    response = RedirectResponse("/accounts", status_code=303)
    response.set_cookie("user", user.username)
    response.set_cookie("role", user.role)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("user")
    response.delete_cookie("role")
    return response
