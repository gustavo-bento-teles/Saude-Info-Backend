from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Unidade_Saude_Medico(Base):
    __tablename__ = "unidade_saude_medico"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_medico: Mapped[int] = mapped_column(ForeignKey("medico.id"), nullable=False)
    id_unidade_saude: Mapped[int] = mapped_column(
        ForeignKey("unidade_saude.id"), nullable=False
    )
    status_medico_unidade_saude: Mapped[bool] = mapped_column(Boolean, nullable=False)