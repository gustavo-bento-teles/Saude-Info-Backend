from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.medicamento_schema import Medicamento_Create
from app.repositories.medicamento_repository import db_criar_medicamento_banco, db_deletar_medicamento_banco
from app.repositories.falta_medicamento_unidade_saude_repository import db_obter_relacao_falta_medicamento_unidade_saude, db_delete_relacao_falta_medicamento_unidade_saude
from app.repositories.falta_medicamento_unidade_saude_repository import db_criar_relacao_falta_medicamento_unidade_saude
from app.services.auth_service import service_get_current_unidade_saude

def service_criar_medicamento(
    db: Session,
    medicamento_create: Medicamento_Create,
    csrf_token: str | None,
    session_token: str | None
):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    medicamento = db_criar_medicamento_banco(db, medicamento_create)
    db_criar_relacao_falta_medicamento_unidade_saude(db, unidade_saude_id, medicamento.id)
    
    return {
        "message": "Medicamento criado com sucesso"
    }
    
def service_deletar_medicamento(
    db: Session,
    medicamento_id: int,
    csrf_token: str | None,
    session_token: str | None
):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    relacao_falta_medicamento_unidade_saude = db_obter_relacao_falta_medicamento_unidade_saude(db, unidade_saude_id, medicamento_id)
    
    if relacao_falta_medicamento_unidade_saude is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não encontrado"
        )
        
    db_delete_relacao_falta_medicamento_unidade_saude(db, unidade_saude_id, medicamento_id)
    db_deletar_medicamento_banco(db, medicamento_id)