from fastapi import FastAPI
from app.modules.accounts.routes import router as accounts_router
from app.modules.persons.routes import router as persons_router
from app.modules.journal.routes import router as journal_router

app = FastAPI()

app.include_router(accounts_router, prefix="/accounts")
app.include_router(persons_router, prefix="/persons")
app.include_router(journal_router, prefix="/journal")

# Web modules
from app.modules.accounts.routes import router as accounts_router
from app.modules.persons.routes import router as persons_router
from app.modules.journal.routes import router as journal_router
from app.modules.reports.routes import router as reports_router
from app.modules.currencies.routes import router as currencies_router
from app.modules.exchange_rates.routes import router as exchange_rates_router
from app.modules.periods.routes import router as periods_router
from app.modules.auth.routes import router as auth_router

# API modules
from app.api.auth import router as api_auth
from app.api.accounts import router as api_accounts
from app.api.persons import router as api_persons
from app.api.journal import router as api_journal
from app.api.reports import router as api_reports
from app.api.currencies import router as api_currencies

app = FastAPI(title="Accounting System")


@app.on_event("startup")
def startup():
    init_db()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/login") or request.url.path.startswith("/api"):
        return await call_next(request)

    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login")

    return await call_next(request)


# Web routes
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(persons_router)
app.include_router(journal_router)
app.include_router(reports_router)
app.include_router(currencies_router)
app.include_router(exchange_rates_router)
app.include_router(periods_router)

# API routes
app.include_router(api_auth)
app.include_router(api_accounts)
app.include_router(api_persons)
app.include_router(api_journal)
app.include_router(api_reports)
app.include_router(api_currencies)


@app.get("/")
def root():
    return RedirectResponse("/accounts")
