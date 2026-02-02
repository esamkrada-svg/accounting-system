from sqlalchemy.orm import Session
from app.database.models import ExchangeRate, Currency


def get_rates(db: Session):
    return db.query(ExchangeRate).order_by(ExchangeRate.effective_date.desc()).all()


def add_rate(db: Session, currency_id: int, rate: float, effective_date):
    rate_obj = ExchangeRate(
        currency_id=currency_id,
        rate=rate,
        effective_date=effective_date
    )
    db.add(rate_obj)
    db.commit()
    return rate_obj
