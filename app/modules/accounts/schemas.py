from pydantic import BaseModel


class AccountCreate(BaseModel):
    code: str
    name: str
    type: str


class AccountOut(BaseModel):
    id: int
    code: str
    name: str
    type: str

    class Config:
        orm_mode = True
