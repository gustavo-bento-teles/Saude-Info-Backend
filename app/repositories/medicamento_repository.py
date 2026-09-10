from sqlalchemy.orm import Session

from app.schemas.medicamento_schema import Medicamento_Create

from app.models.medicamento import Medicamento

def db_criar_medicamento_banco(db: Session, medicamento_create: Medicamento_Create):
    medicamento = Medicamento(
        nome=medicamento_create.nome,
        dosagem=medicamento_create.dosagem,
        forma=medicamento_create.forma
    )
    
    db.add(medicamento)
    db.commit()
    db.refresh(medicamento)
    
    return medicamento