from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response

from app.schemas.medico_schema import Medico_Create
from app.repositories.medico_repository import db_criar_medico_banco
from app.repositories.unidade_saude_medico_repository import db_criar_relacao_unidade_saude_medico
from app.services.auth_service import service_get_current_unidade_saude

def service_criar_medico(
    db: Session,
    response: Response,
    medico_create: Medico_Create,
    csrf_token: str | None,
    session_token: str | None
):
    unidade_saude_id = service_get_current_unidade_saude(db, response, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    
    medico = db_criar_medico_banco(db, medico_create)
    db_criar_relacao_unidade_saude_medico(db, medico.id, unidade_saude_id, False)
    
    return {
        "message": "Médico criado com sucesso",
        "medico": medico
    }