from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Especializacao_Medico(Base):
    __tablename__ = "especializacao_medico"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_medico: Mapped[int] = mapped_column(ForeignKey("medico.id"))
    id_especializacao: Mapped[int] = mapped_column(ForeignKey("especializacao.id"))