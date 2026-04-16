from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Conta(Base):
    __tablename__ = 'contas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    # Relacionamento: Uma conta tem muitas transações
    transacoes: Mapped[list["Transacao"]] = relationship(
        "Transacao", back_populates="conta", cascade="all, delete-orphan"
    )