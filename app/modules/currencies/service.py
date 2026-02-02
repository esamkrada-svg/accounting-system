from sqlalchemy.orm import Session
from app.database.models import Currency


def get_all_currencies(db: Session):
    return db.query(Currency).order_by(Currency.code).all()


def create_currency(db: Session, code: str, name: str):
    currency = Currency(code=code, name=name)
    db.add(currency)
    db.commit()
    db.refresh(currency)
    return currency


def toggle_currency(db: Session, currency_id: int):
    currency = db.query(Currency).get(currency_id)
    if currency:
        currency.active = not currency.active
        db.commit()
    return currency
