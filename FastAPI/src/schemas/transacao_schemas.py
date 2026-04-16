from pydantic import BaseModel, Field


class TransacaoCreate(BaseModel):
    quantidade: float = Field(..., gt=0, description='O valor deve ser maior que zero')