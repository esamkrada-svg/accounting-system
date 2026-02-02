from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()


# -------------------------
# Chart of Accounts
# -------------------------
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # Asset, Liability, Equity, Income, Expense


# -------------------------
# Persons (Customers / Vendors / Others)
# -------------------------
class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)  # customer, vendor, employee, other


# -------------------------
# Currencies
# -------------------------
class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)


# -------------------------
# Journal Header
# -------------------------
class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True)
    entry_no = Column(Integer, index=True)
    date = Column(Date, default=date.today)
    description = Column(String)
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    posted = Column(Boolean, default=False)

    currency = relationship("Currency")
    lines = relationship("JournalLine", back_populates="entry")


# -------------------------
# Journal Lines
# -------------------------
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
