from pydantic import BaseModel

class UnidadeMedica_Create(BaseModel):
    nome_login: str
    nome_exibicao: str

    localizacao_exibicao: str
    localizacao_link_mapa: str
    horario_abertura: str
    horario_fechamento: str