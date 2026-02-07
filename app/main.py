from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

# ================= DATABASE =================
from app.database.db import init_db, SessionLocal
from app.database.seed import create_default_admin

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

# ================= STARTUP =================
@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    try:
        create_default_admin(db)
    finally:
        db.close()

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

    # السماح بالمسارات العامة + API
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
