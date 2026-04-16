from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ContaIn(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=8, max_length=100)

class ContaOut(BaseModel):
    id:int
    name: str
    email: EmailStr
    balance:float

    class Config:
        from_attributes = True

# class TransacaoOut(BaseModel):
#     id: int
#     conta_id: int
#     type: str
#     quantidade: PositiveFloat
#     timestamp: AwareDatetime | NaiveDatetime