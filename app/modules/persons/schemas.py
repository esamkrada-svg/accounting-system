from pydantic import BaseModel


class PersonCreate(BaseModel):
    name: str
    category: str  # customer, vendor, employee, other


class PersonOut(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        orm_mode = True
