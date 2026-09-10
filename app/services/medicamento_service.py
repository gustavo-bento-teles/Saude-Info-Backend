from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.schemas.medicamento_schema import Medicamento_Create
from app.repositories.medicamento_repository import db_criar_medicamento_banco
from app.services.auth_service import service_get_current_unidade_saude, obter_session_cookie, obter_csrf_token

def service_criar_medicamento(
    db: Session,
    medicamento_create: Medicamento_Create,
    csrf_token: str | None = Depends(obter_csrf_token),
    session_token: str | None = Depends(obter_session_cookie)
):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    medicamento = db_criar_medicamento_banco(db, medicamento_create)
    
    return {
        "message": "Medicamento criado com sucesso",
        "medicamento": medicamento
    }