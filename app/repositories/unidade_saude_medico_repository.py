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