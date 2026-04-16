from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256

from src.models.conta_model import Conta
from src.views.conta import ContaIn
from src.auth_utils import get_password_hash

# pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def criar_conta(db: AsyncSession, conta_data: ContaIn):
    # print(conta_data)

    conta_existente = select(Conta).where(Conta.email == conta_data.email)
    resultado = await db.execute(conta_existente)

    if resultado.scalar_one_or_none():
        return None
    
    hashed_pwd = get_password_hash(conta_data.senha)

    nova_conta = Conta(
        name=conta_data.nome,
        email=conta_data.email,
        hashed_password=hashed_pwd,
        balance=0.0
    )

    db.add(nova_conta)

    await db.commit()
    await db.refresh(nova_conta)

    return nova_conta

async def get_conta_por_id(db: AsyncSession, conta_id: int):
    buscar_conta_id = select(Conta).where(Conta.id == conta_id)
    resultado = await db.execute(buscar_conta_id)

    return resultado.scalar_one_or_none()

async def get_conta_por_email(db: AsyncSession, email: str):
    buscar_conta_email = select(Conta).where(Conta.email == email)
    resultado = await db.execute(buscar_conta_email)

    return resultado.scalar_one_or_none()

async def get_all_contas(db: AsyncSession):
    contas = select(Conta)
    resultado = await db.execute(contas)

    return resultado.scalars().all()

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pbkdf2_sha256.verify(senha, senha_hash)