from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base

class Unidade_Saude(Base):
    __tablename__ = "unidade_saude"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome_login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    nome_exibicao: Mapped[str] = mapped_column(String(100), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    localizacao_exibicao: Mapped[str] = mapped_column(String(255), nullable=False)
    localizacao_link_mapa: Mapped[str] = mapped_column(String(255), nullable=True)
    aberto: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    horario_abertura: Mapped[str] = mapped_column(String(20), nullable=False)
    horario_fechamento: Mapped[str] = mapped_column(String(20), nullable=False)

    pessoas_fila_atendimento: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pessoas_atendidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)