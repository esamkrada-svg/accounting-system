from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    type = Column(String)


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True)
    entry_no = Column(Integer, unique=True)
    date = Column(Date, default=date.today)
    description = Column(String)
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    posted = Column(Boolean, default=False)

    currency = relationship("Currency")
    lines = relationship("JournalLine", back_populates="entry")


class JournalLine(Base):
    __tablename__ = "journal_lines"

    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    debit = Column(Float, default=0)
    credit = Column(Float, default=0)

    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account")
    person = relationship("Person")
