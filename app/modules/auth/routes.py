from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# ✅ المصدر الصحيح الوحيد لقاعدة البيانات
from app.database.db import SessionLocal

# ✅ خدمة التحقق
from app.modules.auth.service import authenticate

# ================= ROUTER =================
router = APIRouter(tags=["Auth"])

# ================= TEMPLATES =================
templates = Jinja2Templates(directory="app/templates")

# ================= DB DEPENDENCY =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= LOGIN PAGE =================
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

# ================= LOGIN ACTION =================
@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = authenticate(db, username, password)

    if not user:
        # ❌ فشل تسجيل الدخول
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "اسم المستخدم أو كلمة المرور غير صحيحة",
            }
        )

    # ✅ نجاح تسجيل الدخول
    response = RedirectResponse("/accounts", status_code=303)
    response.set_cookie(key="user", value=user.username, httponly=True)
    response.set_cookie(key="role", value=user.role, httponly=True)
    return response

# ================= LOGOUT =================
@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("user")
    response.delete_cookie("role")
    return response
