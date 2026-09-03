from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Unidade_Saude(Base):
    __tablename__ = "unidade_saude"

    id: Mapped[int] = mapped_column(primary_key=True)

    nome_login: Mapped[str] = mapped_column(String(100), nullable=False)
    nome_exibicao: Mapped[str] = mapped_column(String(100), nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    localizacao: Mapped[str] = mapped_column(String(255), nullable=False)
    aberto: Mapped[bool] = mapped_column(Boolean, nullable=False)
    horario_abertura: Mapped[str] = mapped_column(String(20), nullable=False)
    horario_fechamento: Mapped[str] = mapped_column(String(20), nullable=False)

    pessoas_fila_atendimento: Mapped[int] = mapped_column(Integer, nullable=False)
    pessoas_atendidas: Mapped[int] = mapped_column(Integer, nullable=False)


class Medico(Base):
    __tablename__ = "medico"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)


class Unidade_Saude_Medico(Base):
    __tablename__ = "unidade_saude_medico"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_medico: Mapped[int] = mapped_column(ForeignKey("medico.id"), nullable=False)
    id_unidade_saude: Mapped[int] = mapped_column(
        ForeignKey("unidade_saude.id"), nullable=False
    )
    status_medico_unidade_saude: Mapped[str] = mapped_column(String(30), nullable=False)


class Especializacao(Base):
    __tablename__ = "especializacao"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)


class Especializacao_Medico(Base):
    __tablename__ = "especializacao_medico"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_medico: Mapped[int] = mapped_column(ForeignKey("medico.id"))
    id_especializacao: Mapped[int] = mapped_column(ForeignKey("especializacao.id"))


class Medicamento(Base):
    __tablename__ = "medicamento"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    dosagem: Mapped[str] = mapped_column(String(40), nullable=False)
    forma: Mapped[str] = mapped_column(String(30), nullable=False)


class Falta_Medicamento_Unidade_Saude(Base):
    __tablename__ = "falta_medicamento_unidade_saude"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_unidade_saude: Mapped[int] = mapped_column(ForeignKey("unidade_saude.id"))
    id_medicamento: Mapped[int] = mapped_column(ForeignKey("medicamento.id"))
