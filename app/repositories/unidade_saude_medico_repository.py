from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.unidade_saude_medico import Unidade_Saude_Medico

def db_criar_relacao_unidade_saude_medico(db: Session, medico_id: int, unidade_saude_id: int, status_medico_unidade_saude: bool):
    unidade_saude_medico = Unidade_Saude_Medico(
        id_medico=medico_id,
        id_unidade_saude=unidade_saude_id,
        status_medico_unidade_saude=status_medico_unidade_saude
    )
    
    db.add(unidade_saude_medico)
    db.commit()
    db.refresh(unidade_saude_medico)
    

def db_obter_relacao_unidade_saude_medico(
    db: Session,
    unidade_saude_id: int,
    medico_id: int
) -> Unidade_Saude_Medico | None:
    unidade_saude_medico = db.execute(
        select(Unidade_Saude_Medico)
            .where(
                Unidade_Saude_Medico.id_medico == medico_id,
                Unidade_Saude_Medico.id_unidade_saude == unidade_saude_id
            )
    ).scalar_one_or_none()
    
    return unidade_saude_medico


def db_delete_relacao_unidade_saude_medico(
    db: Session,
    unidade_saude_id: int,
    medico_id: int
):
    unidade_saude_medico = db_obter_relacao_unidade_saude_medico(db, unidade_saude_id, medico_id)
    
    if unidade_saude_medico is None:
        return False
    
    db.delete(unidade_saude_medico)
    db.commit()