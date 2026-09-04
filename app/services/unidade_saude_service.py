from sqlalchemy.orm import Session

from app.repositories.unidade_saude_repository import db_criar_unidade_saude

from app.schemas.unidade_saude import UnidadeSaude_Create

from app.security.criador_senhas import criar_senha_aleatoria
from app.security.hasher import hashear_senha

def criar_unidade_saude(db:Session, unidade_saude_create: UnidadeSaude_Create):
    senha: str = criar_senha_aleatoria()
    senha_hasheada: str = hashear_senha(senha)

    # Falta adicionar no banco de dados

    return {
        "unidade-saude": unidade_saude_create,
        "senha-acesso": senha
    }