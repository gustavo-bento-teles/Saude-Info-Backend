from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Especializacao(Base):
    __tablename__ = "especializacao"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)