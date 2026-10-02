from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.falta_medicamento_unidade_saude import Falta_Medicamento_Unidade_Saude

def db_criar_relacao_falta_medicamento_unidade_saude(
    db: Session,
    unidade_saude_id: int,
    medicamento_id: int
):
    
    falta_medicamento_unidade_saude = Falta_Medicamento_Unidade_Saude(
        id_unidade_saude=unidade_saude_id,
        id_medicamento=medicamento_id
    )
    
    db.add(falta_medicamento_unidade_saude)
    db.commit()
    db.refresh(falta_medicamento_unidade_saude)


def db_obter_relacao_falta_medicamento_unidade_saude(
    db: Session,
    unidade_saude_id: int,
    medicamento_id: int
) -> Falta_Medicamento_Unidade_Saude | None:
    falta_medicamento_unidade_saude = db.execute(
        select(Falta_Medicamento_Unidade_Saude)
            .where(
                Falta_Medicamento_Unidade_Saude.id_medicamento == medicamento_id,
                Falta_Medicamento_Unidade_Saude.id_unidade_saude == unidade_saude_id
            )
    ).scalar_one_or_none()
    
    return falta_medicamento_unidade_saude


def db_delete_relacao_falta_medicamento_unidade_saude(
    db: Session,
    unidade_saude_id: int,
    medicamento_id: int
):
    falta_medicamento_unidade_saude = db_obter_relacao_falta_medicamento_unidade_saude(db, unidade_saude_id, medicamento_id)
    
    if falta_medicamento_unidade_saude is None:
        return False
    
    db.delete(falta_medicamento_unidade_saude)
    db.commit()