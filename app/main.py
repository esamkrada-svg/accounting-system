from fastapi import FastAPI
from app.database.database import init_db

app = FastAPI(
    title="Accounting System",
    description="Modular Accounting System (Arabic / English)",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Accounting system is running"
    }
