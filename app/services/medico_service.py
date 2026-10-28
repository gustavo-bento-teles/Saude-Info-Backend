from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.medico_schema import Medico_Create
from app.repositories.medico_repository import db_criar_medico_banco, db_deletar_medico_banco
from app.repositories.unidade_saude_medico_repository import db_criar_relacao_unidade_saude_medico, db_delete_relacao_unidade_saude_medico, db_obter_relacao_unidade_saude_medico, db_atualizar_status_medico_relacao_unidade_saude_medico_by_id
from app.services.auth_service import service_get_current_unidade_saude

def service_criar_medico(
    db: Session,
    medico_create: Medico_Create,
    csrf_token: str | None,
    session_token: str | None
):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    
    medico = db_criar_medico_banco(db, medico_create)
    db_criar_relacao_unidade_saude_medico(db, medico.id, unidade_saude_id, False)
    
    return {
        "detail": "Médico criado com sucesso"
    }


def service_deletar_medico(
    db: Session,
    medico_id: int,
    csrf_token: str | None,
    session_token: str | None
):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    relacao_unidade_saude_medico = db_obter_relacao_unidade_saude_medico(db, unidade_saude_id, medico_id)
    
    if relacao_unidade_saude_medico is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não encontrado"
        )
    
    db_delete_relacao_unidade_saude_medico(db, unidade_saude_id, medico_id)
    db_deletar_medico_banco(db, medico_id)
    
    return {
            "detail": "Médico deletado com sucesso"
        }
    

def service_atualizar_status_medico(
    db: Session,
    medico_id: int,
    status_medico: bool,
    csrf_token: str | None,
    session_token: str | None
):
    unidade_saude_id = service_get_current_unidade_saude(db, csrf_token, session_token)
    
    if unidade_saude_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    
    if not db_atualizar_status_medico_relacao_unidade_saude_medico_by_id(db, unidade_saude_id, medico_id, status_medico):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relação de médico com unidade de saude não encontrada"
        )
        
    return {
        "detail": "Atualizado com sucesso"
    }