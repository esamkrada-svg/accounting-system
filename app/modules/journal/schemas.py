from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class JournalLineCreate(BaseModel):
    account_id: int
    debit: float = 0
    credit: float = 0
    person_id: Optional[int] = None


class JournalEntryCreate(BaseModel):
    entry_no: int
    date: date
    description: str
    currency_id: int
    lines: List[JournalLineCreate]
