from pydantic import BaseModel

class UnidadeSaude_Busca_Response(BaseModel):
    nome_login: str
    nome_exibicao: str
    
    localizacao_exibicao: str
    localizacao_link_mapa: str
    aberto: bool
    horario_abertura: str
    horario_fechamento: str
    
    pessoas_fila_atendimento: int
    pessoas_atendidas: int

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