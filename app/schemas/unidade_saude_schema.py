from pydantic import BaseModel, ConfigDict

from app.schemas.medico_schema import Medico_Response
from app.schemas.medicamento_schema import Medicamento_Response

# ================
# Entrada de dados
# ================

class UnidadeSaude_Create(BaseModel):
    nome_login: str
    nome_exibicao: str

    localizacao_exibicao: str
    localizacao_link_mapa: str
    horario_abertura: str
    horario_fechamento: str


class UnidadeSaude_Login(BaseModel):
    nome_login: str
    senha: str


class UnidadeSaude_Response(BaseModel):
    id: int
    nome_exibicao: str
    localizacao_exibicao: str
    localizacao_link_mapa: str
    aberto: bool
    horario_abertura: str
    horario_fechamento: str
    pessoas_fila_atendimento: int
    pessoas_atendidas: int

class UnidadeSaude_Detailed_Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nome_exibicao: str
    localizacao_exibicao: str
    localizacao_link_mapa: str
    aberto: bool
    horario_abertura: str
    horario_fechamento: str
    pessoas_fila_atendimento: int
    pessoas_atendidas: int
    
    medicos: list[Medico_Response]
    medicamentos: list[Medicamento_Response]