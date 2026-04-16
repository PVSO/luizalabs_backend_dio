from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base


class Transacao(Base):
    __tablename__ = 'transacoes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conta_id: Mapped[int] = mapped_column(ForeignKey('contas.id'), nullable=False)
    
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    quantidade: Mapped[float] = mapped_column(Float, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    conta: Mapped['Conta'] = relationship('Conta', back_populates='transacoes')