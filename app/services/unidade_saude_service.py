from sqlalchemy.orm import Session

from app.repositories.unidade_saude_repository import db_criar_unidade_saude, db_buscar_unidade_saude_nome_login

from app.schemas.unidade_saude_schema import UnidadeSaude_Create, UnidadeSaude_Login, UnidadeSaude_Busca_Response

from app.security.criador_strings import criar_string_aleatoria
from app.security.hasher import hashear_string

def criar_unidade_saude_service(db:Session, unidade_saude_create: UnidadeSaude_Create):
    senha: str = criar_string_aleatoria(24)
    senha_hasheada: str = hashear_string(senha)

    unidade_saude_criada = db_criar_unidade_saude(db, unidade_saude_create, senha_hasheada)    

    if unidade_saude_criada != None:
        return {
            "unidade-saude": unidade_saude_create,
            "senha-acesso": senha
        }

    return {
        "detail": "Usuário já existente"
    }

def buscar_unidade_saude_nome_login_service(
    db: Session,
    unidade_saude_login: UnidadeSaude_Login
) -> UnidadeSaude_Busca_Response | None:
    resultado_busca = db_buscar_unidade_saude_nome_login(db, unidade_saude_login)

    if resultado_busca is None:
        return {
            "detail": "Unidade de saúde não encontrada"
        }

    # Falta colocar validação do hash da senha para retornar os dados

    return UnidadeSaude_Busca_Response(
        nome_login=resultado_busca.nome_login,
        nome_exibicao=resultado_busca.nome_exibicao,
        localizacao_exibicao=resultado_busca.localizacao_exibicao,
        localizacao_link_mapa=resultado_busca.localizacao_link_mapa,
        aberto=resultado_busca.aberto,
        horario_abertura=resultado_busca.horario_abertura,
        horario_fechamento=resultado_busca.horario_fechamento,
        pessoas_fila_atendimento=resultado_busca.pessoas_fila_atendimento,
        pessoas_atendidas=resultado_busca.pessoas_atendidas
    )