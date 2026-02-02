from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.database.database import init_db

from app.modules.accounts.routes import router as accounts_router
from app.modules.persons.routes import router as persons_router
from app.modules.journal.routes import router as journal_router
from app.modules.reports.routes import router as reports_router
from app.modules.currencies.routes import router as currencies_router
from app.modules.periods.routes import router as periods_router
from app.modules.auth.routes import router as auth_router

app = FastAPI(title="Accounting System")


@app.on_event("startup")
def startup():
    init_db()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/login"):
        return await call_next(request)

    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/login")

    return await call_next(request)


app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(persons_router)
app.include_router(journal_router)
app.include_router(reports_router)
app.include_router(currencies_router)
app.include_router(periods_router)


@app.get("/")
def root():
    return RedirectResponse("/accounts")
