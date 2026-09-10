from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.medico_schema import Medico_Create, Medico_Response
from app.models.medico import Medico

def db_criar_medico_banco(db: Session, medico_create: Medico_Create):
    medico = Medico(
        nome=medico_create.nome,
        especializacao=medico_create.especializacao
    )
    
    db.add(medico)
    db.commit()
    db.refresh(medico)
    
    return medico