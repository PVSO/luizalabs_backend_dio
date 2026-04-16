from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from src.models.conta_model import Conta
from src.models.transacao_model import Transacao

class TransacaoService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def registrar_transacao(self, conta_id: int, quantidade: float, tipo: str):
        # Se for saque, precisamos validar o saldo aqui
        if tipo == "saque":
            saldo_atual = await self.calcular_saldo(conta_id)
            if saldo_atual < quantidade:
                raise HTTPException(status_code=400, detail="Saldo insuficiente")
            
            # No banco, você pode optar por salvar saque como valor negativo 
            # ou manter positivo e subtrair na lógica de saldo. 
            # Seguiremos a lógica de salvar o valor absoluto e tratar o 'tipo'.
        
        nova_transacao = Transacao(
            conta_id=conta_id,
            tipo=tipo,
            quantidade=quantidade
        )
        
        self.db.add(nova_transacao)
        await self.db.commit()
        await self.db.refresh(nova_transacao)
        return nova_transacao


    async def calcular_saldo(self, conta_id: int) -> float:
        # Lógica para somar depositos e subtrair saques
        result = await self.db.execute(
            select(Transacao).where(Transacao.conta_id == conta_id)
        )

        transacoes = result.scalars().all()
        
        saldo = 0.0
        for t in transacoes:
            if t.tipo == "deposito":
                saldo += t.quantidade
            else:
                saldo -= t.quantidade
        return saldo


    async def buscar_extrato(self, conta_id: int):
        """Retorna a lista de todas as transações de uma conta específica."""
        query = select(Transacao).where(Transacao.conta_id == conta_id).order_by(Transacao.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()


    async def obter_status_financeiro_resumido(self, user: Conta):
        # Aqui o service poderia buscar algo específico, 
        # mas por enquanto apenas formata um status básico
        return {
            "usuario": user.name,
            "saldo_atual": user.balance,
            "status": "autenticado e ativo"
        }