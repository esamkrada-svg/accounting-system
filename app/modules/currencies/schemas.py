from pydantic import BaseModel


class CurrencyCreate(BaseModel):
    code: str
    name: str


class CurrencyOut(BaseModel):
    id: int
    code: str
    name: str
    active: bool

    class Config:
        orm_mode = True
