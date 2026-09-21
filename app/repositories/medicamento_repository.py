from sqlalchemy.orm import Session
from sqlalchemy import delete, select

from app.schemas.medicamento_schema import Medicamento_Create

from app.models.medicamento import Medicamento

def db_criar_medicamento_banco(db: Session, medicamento_create: Medicamento_Create) -> Medicamento:
    medicamento = Medicamento(
        nome=medicamento_create.nome,
        dosagem=medicamento_create.dosagem,
        forma=medicamento_create.forma
    )
    
    db.add(medicamento)
    db.commit()
    db.refresh(medicamento)
    
    return medicamento

def db_obter_medicamento_banco(db: Session, medicamento_id: int) -> Medicamento | None:
    medicamento = db.execute(
        select(Medicamento)
            .where(Medicamento.id == medicamento_id)
    ).scalar_one_or_none()
    
    return medicamento

def db_deletar_medicamento_banco(db: Session, medicamento_id: int) -> bool:
    medicamento = db_obter_medicamento_banco(db, medicamento_id)
    
    if medicamento is None:
        return False
    
    db.delete(medicamento)
    db.commit()
    
    return True