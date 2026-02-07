from app.database.db import SessionLocal
from app.database.models import Currency


def seed_currencies():
    db = SessionLocal()

    try:
        currencies = [
            # code , name_ar , symbol , is_base
            ("YER", "الريال اليمني", "﷼", True),
            ("USD", "الدولار الأمريكي", "$", False),
            ("SAR", "الريال السعودي", "﷼", False),
            ("EUR", "اليورو", "€", False),
            ("GBP", "الجنيه الإسترليني", "£", False),
            ("EGP", "الجنيه المصري", "£", False),
            ("AED", "الدرهم الإماراتي", "د.إ", False),
            ("OMR", "الريال العماني", "﷼", False),
            ("QAR", "الريال القطري", "﷼", False),
            ("KWD", "الدينار الكويتي", "د.ك", False),
        ]

        for code, name, symbol, is_base in currencies:
            exists = db.query(Currency).filter(Currency.code == code).first()
            if not exists:
                db.add(
                    Currency(
                        code=code,
                        name=name,
                        symbol=symbol,
                        is_base=is_base
                    )
                )

        db.commit()
        print("✅ Currencies seeded successfully")

    finally:
        db.close()


if __name__ == "__main__":
    seed_currencies()
