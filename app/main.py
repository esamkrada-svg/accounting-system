from fastapi import FastAPI
from app.database.database import init_db
from app.modules.accounts.routes import router as accounts_router
from app.modules.persons.routes import router as persons_router
from app.modules.journal.routes import router as journal_router
from app.modules.reports.routes import router as reports_router

app = FastAPI(
    title="Accounting System",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(accounts_router)
app.include_router(persons_router)
app.include_router(journal_router)
app.include_router(reports_router)


@app.get("/")
def root():
    return {"status": "ok"}
