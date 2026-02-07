from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

# ================= DATABASE =================
from app.database.db import init_db, SessionLocal
from app.database.models import Account

# ================= WEB MODULES =================
from app.modules.auth.routes import router as auth_router
from app.modules.accounts.routes import router as accounts_router
from app.modules.persons.routes import router as persons_router
from app.modules.journal.routes import router as journal_router
from app.modules.reports.routes import router as reports_router
from app.modules.currencies.routes import router as currencies_router
from app.modules.exchange_rates.routes import router as exchange_rates_router
from app.modules.periods.routes import router as periods_router

# ================= API MODULES =================
from app.api.auth import router as api_auth
from app.api.accounts import router as api_accounts
from app.api.persons import router as api_persons
from app.api.journal import router as api_journal
from app.api.reports import router as api_reports
from app.api.currencies import router as api_currencies

# ================= APP =================
app = FastAPI(title="Accounting System")

# ================= SEED CHART OF ACCOUNTS =================
def seed_chart_of_accounts():
    db = SessionLocal()
    try:
        accounts = [
            ("1000", "الأصول", "Asset"),
            ("1100", "الصندوق", "Asset"),
            ("1110", "البنك", "Asset"),
            ("1120", "عهدة موظفين", "Asset"),
            ("1130", "ذمم مدينة", "Asset"),
            ("1140", "مصروفات مدفوعة مقدمًا", "Asset"),
            ("1150", "مخزون", "Asset"),
            ("1200", "الأصول الثابتة", "Asset"),
            ("1210", "أثاث", "Asset"),
            ("1220", "أجهزة ومعدات", "Asset"),
            ("1230", "مركبات", "Asset"),
            ("1240", "مجمع الإهلاك", "Asset"),

            ("2000", "الالتزامات", "Liability"),
            ("2100", "ذمم دائنة", "Liability"),
            ("2110", "مستحقات موظفين", "Liability"),
            ("2120", "مصروفات مستحقة", "Liability"),
            ("2130", "سلف مستلمة", "Liability"),
            ("2200", "قروض طويلة الأجل", "Liability"),

            ("3000", "حقوق الملكية", "Equity"),
            ("3100", "رأس المال", "Equity"),
            ("3200", "فائض / عجز مرحل", "Equity"),

            ("4000", "الإيرادات", "Revenue"),
            ("4100", "إيرادات تشغيلية", "Revenue"),
            ("4200", "إيرادات خدمات", "Revenue"),
            ("4300", "إيرادات أخرى", "Revenue"),

            ("5000", "المصروفات", "Expense"),
            ("5100", "رواتب وأجور", "Expense"),
            ("5110", "بدلات", "Expense"),
            ("5120", "تأمينات", "Expense"),
            ("5200", "إيجار", "Expense"),
            ("5210", "كهرباء ومياه", "Expense"),
            ("5220", "اتصالات وإنترنت", "Expense"),
            ("5230", "قرطاسية", "Expense"),
            ("5240", "صيانة", "Expense"),
            ("5300", "مصروفات بنكية", "Expense"),
            ("5310", "إهلاك", "Expense"),
            ("5320", "مصروفات متنوعة", "Expense"),
        ]

        for code, name, acc_type in accounts:
            exists = db.query(Account).filter(Account.code == code).first()
            if not exists:
                db.add(Account(code=code, name=name, type=acc_type))

        db.commit()
        print("✅ Chart of Accounts seeded successfully")

    finally:
        db.close()

# ================= STARTUP =================
@app.on_event("startup")
def startup():
    init_db()
    seed_chart_of_accounts()

# ================= MIDDLEWARE =================
PUBLIC_PATHS = (
    "/login",
    "/docs",
    "/openapi.json",
    "/redoc",
)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path

    if path.startswith(PUBLIC_PATHS) or path.startswith("/api"):
        return await call_next(request)

    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login")

    return await call_next(request)

# ================= WEB ROUTES =================
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(persons_router)
app.include_router(journal_router)
app.include_router(reports_router)
app.include_router(currencies_router)
app.include_router(exchange_rates_router)
app.include_router(periods_router)

# ================= API ROUTES =================
app.include_router(api_auth, prefix="/api")
app.include_router(api_accounts, prefix="/api")
app.include_router(api_persons, prefix="/api")
app.include_router(api_journal, prefix="/api")
app.include_router(api_reports, prefix="/api")
app.include_router(api_currencies, prefix="/api")

# ================= ROOT =================
@app.get("/")
def root():
    return RedirectResponse("/accounts")
