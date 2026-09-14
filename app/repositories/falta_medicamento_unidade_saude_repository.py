from sqlalchemy.orm import Session

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