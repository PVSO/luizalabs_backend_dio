from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from src.views.conta import ContaIn, ContaOut
from src.services import conta_service


rota = APIRouter()

@rota.post('/criar', response_model=ContaOut, status_code=status.HTTP_201_CREATED)
async def criar_conta(
    conta_data: ContaIn,
    db: AsyncSession = Depends(get_db)
):
    nova_conta = await conta_service.criar_conta(db, conta_data)

    if not nova_conta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Já existe outra conta com o mesmo e-mail.')

    return nova_conta


@rota.get('/contas', response_model=List[ContaOut])
async def contas(
    db: AsyncSession = Depends(get_db)
):
    contas = await conta_service.get_all_contas(db)

    return contas


@rota.get('/{conta_id}', response_model=ContaOut, status_code=status.HTTP_200_OK)
async def ver_conta(
    conta_id: int,
    db: AsyncSession = Depends(get_db)
):
    account = await conta_service.get_conta_por_id(db, conta_id)

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Conta não encontrada.')

    return account