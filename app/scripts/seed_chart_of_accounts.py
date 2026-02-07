from app.database.db import SessionLocal
from app.database.models import Account


def seed_chart_of_accounts():
    db = SessionLocal()

    try:
        accounts = [
            # ===== الأصول =====
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

            # ===== الالتزامات =====
            ("2000", "الالتزامات", "Liability"),
            ("2100", "ذمم دائنة", "Liability"),
            ("2110", "مستحقات موظفين", "Liability"),
            ("2120", "مصروفات مستحقة", "Liability"),
            ("2130", "سلف مستلمة", "Liability"),
            ("2200", "قروض طويلة الأجل", "Liability"),

            # ===== حقوق الملكية =====
            ("3000", "حقوق الملكية", "Equity"),
            ("3100", "رأس المال", "Equity"),
            ("3200", "فائض / عجز مرحل", "Equity"),

            # ===== الإيرادات =====
            ("4000", "الإيرادات", "Revenue"),
            ("4100", "إيرادات تشغيلية", "Revenue"),
            ("4200", "إيرادات خدمات", "Revenue"),
            ("4300", "إيرادات أخرى", "Revenue"),

            # ===== المصروفات =====
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
            exists = db.query(Account).filter(Account.code == code).first()
            if not exists:
                db.add(Account(code=code, name=name, type=acc_type))

        db.commit()
        print("✅ Chart of Accounts seeded successfully")

    finally:
        db.close()


if __name__ == "__main__":
    seed_chart_of_accounts()
