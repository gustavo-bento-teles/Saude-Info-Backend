from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.unidade_saude import Unidade_Saude

from app.schemas.unidade_saude import UnidadeSaude_Create

def db_criar_unidade_saude(
    db: Session,
    unidade_saude_create: UnidadeSaude_Create,
    senha_hasheada: str, 
    unidade_aberta: bool
) -> Unidade_Saude:
    
    unidade_saude: Unidade_Saude = Unidade_Saude(
        nome_login=unidade_saude_create.nome_login,
        nome_exibicao=unidade_saude_create.nome_exibicao,
        senha=senha_hasheada,
        localizacao_exibicao=unidade_saude_create.localizacao_exibicao,
        localizacao_link_mapa=unidade_saude_create.localizacao_link_mapa,
        aberto=unidade_aberta,
        horario_abertura=unidade_saude_create.horario_abertura,
        horario_fechamento=unidade_saude_create.horario_fechamento,
        pessoas_fila_atendimento=0,
        pessoas_atendidas=0
    )

    db.add(unidade_saude)
    db.commit()
    db.refresh(unidade_saude)

    return unidade_saude