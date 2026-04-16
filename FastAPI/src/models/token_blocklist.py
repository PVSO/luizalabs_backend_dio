from datetime import datetime, timezone
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class TokenBlocklist(Base):
    __tablename__ = 'token_blocklist'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    jti: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )