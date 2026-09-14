from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response

from app.schemas.medicamento_schema import Medicamento_Create
from app.repositories.medicamento_repository import db_criar_medicamento_banco
from app.repositories.falta_medicamento_unidade_saude_repository import db_criar_relacao_falta_medicamento_unidade_saude
from app.services.auth_service import service_get_current_unidade_saude

def service_criar_medicamento(
    db: Session,
    response: Response,
    medicamento_create: Medicamento_Create,
    csrf_token: str | None,
    session_token: str | None
):
    unidade_saude_id = service_get_current_unidade_saude(db, response, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    medicamento = db_criar_medicamento_banco(db, medicamento_create)
    db_criar_relacao_falta_medicamento_unidade_saude(db, unidade_saude_id, medicamento.id)
    
    return {
        "message": "Medicamento criado com sucesso",
        "medicamento": medicamento
    }