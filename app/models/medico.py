from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Medico(Base):
    __tablename__ = "medico"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)