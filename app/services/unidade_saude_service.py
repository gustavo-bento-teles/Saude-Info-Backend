from sqlalchemy.orm import Session

from fastapi import HTTPException, status, Response

from app.repositories.unidade_saude_repository import db_criar_unidade_saude, db_buscar_unidade_saude_nome_login, db_listar_unidades_saude, db_buscar_unidade_saude_by_id, db_atualizar_dados_unidade_saude_by_id

from app.schemas.unidade_saude_schema import UnidadeSaude_Create, UnidadeSaude_Login, UnidadeSaude_Response, UnidadeSaude_Detailed_Response, UnidadeSaude_Update

from app.security.criador_strings import criar_string_aleatoria
from app.security.hasher import hashear_string, verificar_hash

def service_criar_unidade_saude(db:Session, unidade_saude_create: UnidadeSaude_Create):
    senha: str = criar_string_aleatoria(24)
    senha_hasheada: str = hashear_string(senha)

    unidade_saude_criada = db_criar_unidade_saude(db, unidade_saude_create, senha_hasheada)    

    if unidade_saude_criada is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário já existente"
        )

    return {
        "unidade-saude": unidade_saude_create,
        "senha-acesso": senha
    }



def service_buscar_unidade_saude_by_nome_login(
    db: Session,
    unidade_saude_login: UnidadeSaude_Login
) -> int | None:
    resultado_busca = db_buscar_unidade_saude_nome_login(db, unidade_saude_login)

    if resultado_busca is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nome de login e/ou senha incorreto(s)"
        )

    if not verificar_hash(unidade_saude_login.senha, resultado_busca.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de login e/ou senha incorreto(s)"
        )

    return resultado_busca.id


def service_listar_unidades_saude(db: Session) -> list[UnidadeSaude_Response]:
    unidades_saude = db_listar_unidades_saude(db)
    
    if len(unidades_saude) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma unidade de saúde ainda"
        )
        
    return unidades_saude

def service_buscar_unidade_saude_by_id(db: Session, unidade_saude_id: int) -> UnidadeSaude_Detailed_Response | None:
    unidade_saude = db_buscar_unidade_saude_by_id(db, unidade_saude_id)
    
    if unidade_saude is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade de saúde não encontrada"
        )
    
    return unidade_saude


def service_atualizar_dados_unidade_saude(
    db: Session,
    unidade_saude_id: int,
    unidade_saude_update: UnidadeSaude_Update
):
    unidade_dados = unidade_saude_update.model_dump(exclude_unset=True)
    
    if not db_atualizar_dados_unidade_saude_by_id(db, unidade_saude_id, unidade_dados):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return {
        "detail": "Atualizado com sucesso"
    }