from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from src.auth_utils import get_current_user
from src.models.conta_model import Conta
from src.services.transacao_service import TransacaoService
from src.schemas.transacao_schemas import TransacaoCreate

rota = APIRouter(tags=["transacoes"])

Session = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[Conta, Depends(get_current_user)]

async def get_transacao_service(session: Session):
    return TransacaoService(session)

TransServ = Annotated[TransacaoService, Depends(get_transacao_service)]

@rota.get("/verificar-login")
async def verificar_status_usuario(
    user: CurrentUser, 
    service: TransServ
):
    """
    Rota para verificar se o token é válido e o usuário está logado.
    Utiliza o TransacaoService para retornar um resumo da conta.
    """
    # A lógica de "está logado?" já foi resolvida pelo CurrentUser (Dependência)
    status = await service.obter_status_financeiro_resumido(user)
    return status


@rota.post("/depositar", status_code=status.HTTP_201_CREATED)
async def realizar_deposito(
    dados: TransacaoCreate,
    user: CurrentUser,
    service: TransServ
):
    """
    Registra um depósito na conta do usuário logado.
    """
    # Note que passamos 'quantidade' e definimos o tipo como 'deposito'
    nova_transacao = await service.registrar_transacao(
        conta_id=user.id, 
        quantidade=dados.quantidade, 
        tipo="deposito"
    )
    return {"message": "Depósito realizado", "detalhes": nova_transacao}


@rota.post("/sacar")
async def realizar_saque(
    dados: TransacaoCreate,
    user: CurrentUser,
    service: TransServ
):
    """
    Registra um saque, validando o saldo antes no Service.
    """
    nova_transacao = await service.registrar_transacao(
        conta_id=user.id, 
        quantidade=dados.quantidade, 
        tipo="saque"
    )
    return {"message": "Saque realizado", "detalhes": nova_transacao}


@rota.get("/extrato")
async def exibir_extrato(
    user: CurrentUser,
    service: TransServ
):
    """Retorna o histórico de transações do usuário."""
    return await service.buscar_extrato(conta_id=user.id)