from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.medico_schema import Medico_Create

from app.models.medico import Medico

def db_criar_medico_banco(db: Session, medico_create: Medico_Create) -> Medico:
    medico = Medico(
        nome=medico_create.nome,
        especializacao=medico_create.especializacao
    )
    
    db.add(medico)
    db.commit()
    db.refresh(medico)
    
    return medico


def db_obter_medico_banco(db: Session, medico_id: int) -> Medico | None:
    medico = db.execute(
        select(Medico)
            .where(Medico.id == medico_id)
    ).scalar_one_or_none()
    
    return medico

def db_deletar_medico_banco(db: Session, medico_id: int) -> bool:
    medico = db_obter_medico_banco(db, medico_id)
    
    if medico is None:
        return False
    
    db.delete(medico)
    db.commit()
    
    return True