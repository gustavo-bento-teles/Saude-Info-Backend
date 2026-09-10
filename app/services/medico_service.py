from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.schemas.medico_schema import Medico_Create
from app.repositories.medico_repository import db_criar_medico_banco
from app.services.auth_service import service_get_current_unidade_saude

from app.services.auth_service import obter_session_cookie

def service_criar_medico(db: Session, medico_create: Medico_Create, csrf_token: str, session_token: str | None = Depends(obter_session_cookie)):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    
    medico = db_criar_medico_banco(db, medico_create)
    
    return {
        "message": "Médico criado com sucesso",
        "medico": medico
    }