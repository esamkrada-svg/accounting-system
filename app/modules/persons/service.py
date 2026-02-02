from sqlalchemy.orm import Session
from app.database.models import Person


def get_all_persons(db: Session):
    return db.query(Person).order_by(Person.name).all()


def create_person(db: Session, name: str, category: str):
    person = Person(
        name=name,
        category=category
    )
    db.add(person)
    db.commit()
    db.refresh(person)
    return person
