from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Falta_Medicamento_Unidade_Saude(Base):
    __tablename__ = "falta_medicamento_unidade_saude"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_unidade_saude: Mapped[int] = mapped_column(ForeignKey("unidade_saude.id"))
    id_medicamento: Mapped[int] = mapped_column(ForeignKey("medicamento.id"))