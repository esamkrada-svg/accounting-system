from sqlalchemy.orm import Session
from app.database.models import Account


def get_all_accounts(db: Session):
    return db.query(Account).order_by(Account.code).all()


def create_account(db: Session, code: str, name: str, type: str):
    account = Account(
        code=code,
        name=name,
        type=type
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account
