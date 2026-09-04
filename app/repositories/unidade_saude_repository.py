from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.unidade_saude import Unidade_Saude

from app.schemas.unidade_saude_schema import UnidadeSaude_Create, UnidadeSaude_Login

def db_criar_unidade_saude(
    db: Session,
    unidade_saude_create: UnidadeSaude_Create,
    senha_hasheada: str
) -> UnidadeSaude_Create | None:
      
    existente = db.scalar(
        select(Unidade_Saude).where(
            Unidade_Saude.nome_login == unidade_saude_create.nome_login
        )
    )

    if existente:
        return None

    unidade_saude: Unidade_Saude = Unidade_Saude(
        nome_login=unidade_saude_create.nome_login,
        nome_exibicao=unidade_saude_create.nome_exibicao,
        senha=senha_hasheada,
        localizacao_exibicao=unidade_saude_create.localizacao_exibicao,
        localizacao_link_mapa=unidade_saude_create.localizacao_link_mapa,
        aberto=False,
        horario_abertura=unidade_saude_create.horario_abertura,
        horario_fechamento=unidade_saude_create.horario_fechamento,
        pessoas_fila_atendimento=0,
        pessoas_atendidas=0
    )

    db.add(unidade_saude)
    db.commit()
    db.refresh(unidade_saude)

    return unidade_saude

def db_buscar_unidade_saude_nome_login(
    db: Session,
    unidade_saude_login: UnidadeSaude_Login
) -> Unidade_Saude | None:
    
    resultado_busca = db.execute(
        select(Unidade_Saude)
            .where(Unidade_Saude.nome_login == unidade_saude_login.nome_login)
    )
    return resultado_busca.scalar_one_or_none()