from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Medicamento(Base):
    __tablename__ = "medicamento"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    dosagem: Mapped[str] = mapped_column(String(40), nullable=False)
    forma: Mapped[str] = mapped_column(String(30), nullable=False)