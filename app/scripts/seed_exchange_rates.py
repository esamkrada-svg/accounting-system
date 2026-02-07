from datetime import date
from app.database.db import SessionLocal
from app.database.models import Currency, ExchangeRate


def seed_exchange_rates():
    db = SessionLocal()

    try:
        # جلب العملة الأساسية
        base_currency = db.query(Currency).filter(Currency.is_base == True).first()
        if not base_currency:
            print("❌ No base currency defined")
            return

        # أسعار صرف افتراضية (مقابل العملة الأساسية)
        rates = [
            # code , rate
            ("USD", 1500),
            ("SAR", 400),
            ("EUR", 1650),
            ("GBP", 1900),
            ("EGP", 50),
            ("AED", 410),
            ("OMR", 3900),
            ("QAR", 410),
            ("KWD", 4900),
        ]

        for code, rate in rates:
            currency = db.query(Currency).filter(Currency.code == code).first()
            if not currency:
                continue

            # لا نُنشئ سعر للعملة الأساسية
            if currency.is_base:
                continue

            exists = (
                db.query(ExchangeRate)
                .filter(
                    ExchangeRate.currency_id == currency.id,
                    ExchangeRate.effective_date == date.today()
                )
                .first()
            )

            if not exists:
                db.add(
                    ExchangeRate(
                        currency_id=currency.id,
                        rate=rate,
                        effective_date=date.today()
                    )
                )

        db.commit()
        print("✅ Exchange rates seeded successfully")

    finally:
        db.close()


if __name__ == "__main__":
    seed_exchange_rates()
