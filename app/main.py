from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

# ================= DATABASE =================
from app.database.db import init_db, SessionLocal
from app.database.models import Account, Currency, JournalEntry

# ================= SEED CURRENCIES =================
from app.scripts.seed_currencies import seed_currencies

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

# ================= ERROR MIDDLEWARE =================
from app.core.error_middleware import ErrorCaptureMiddleware
app.add_middleware(ErrorCaptureMiddleware)

# ================= SEED CHART OF ACCOUNTS =================
def seed_chart_of_accounts():
    db = SessionLocal()
    try:
        if db.query(Account).first():
            return

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
            db.add(Account(code=code, name=name, type=acc_type))

        db.commit()
    finally:
        db.close()


# ================= SYSTEM OPENING ENTRY =================
def ensure_system_opening_entry():
    db = SessionLocal()
    try:
        exists = (
            db.query(JournalEntry)
            .filter(JournalEntry.entry_no == 0)
            .first()
        )
        if exists:
            return

        base_currency = db.query(Currency).filter(Currency.is_base == True).first()
        if not base_currency:
            return

        entry = JournalEntry(
            entry_no=0,
            description="System Opening Balance",
            currency_id=base_currency.id,
            posted=True
        )
        db.add(entry)
        db.commit()
    finally:
        db.close()


# ================= STARTUP =================
@app.on_event("startup")
def startup():
    init_db()
    seed_chart_of_accounts()

    db = SessionLocal()
    try:
        if not db.query(Currency).first():
            seed_currencies()
    finally:
        db.close()

    ensure_system_opening_entry()


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

# ✅ AI Error API (مرة واحدة فقط)
from app.api.dev_ai_errors import router as dev_ai_errors_router
app.include_router(dev_ai_errors_router)

from app.api.dev_ai import router as dev_ai_router
app.include_router(dev_ai_router)

from app.api.ai_debug import router as api_ai_debug
app.include_router(api_ai_debug, prefix="/api")
from app.api.dev_ai_auto import router as dev_ai_auto_router
app.include_router(dev_ai_auto_router, prefix="/api")
from app.api.dev_ai_context import router as dev_ai_context_router
app.include_router(dev_ai_context_router)
# ================= ROOT =================
@app.get("/")
def root():
    return RedirectResponse("/accounts")
