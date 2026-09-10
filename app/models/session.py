from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Session(Base):
    __tablename__ = "session"
    
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    csrf_token: Mapped[str] = mapped_column(String(64), nullable=False)
    
    unidade_saude_id: Mapped[int] = mapped_column(
        ForeignKey("unidade_saude.id"), nullable=False
    )
    
    expira_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )