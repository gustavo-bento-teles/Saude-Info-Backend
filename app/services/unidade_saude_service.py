from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.repositories.unidade_saude_repository import db_criar_unidade_saude, db_buscar_unidade_saude_nome_login

from app.schemas.unidade_saude_schema import UnidadeSaude_Create, UnidadeSaude_Login

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
            detail="Unidade de saúde não encontrada"
        )

    if not verificar_hash(unidade_saude_login.senha, resultado_busca.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta"
        )

    return resultado_busca.id