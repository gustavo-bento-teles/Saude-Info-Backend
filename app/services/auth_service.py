from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response, Cookie

from sqlalchemy.orm import Session
from app.schemas.unidade_saude_schema import UnidadeSaude_Login, UnidadeSaude_Detailed_Response
from app.services.unidade_saude_service import service_buscar_unidade_saude_by_nome_login
from app.repositories.session_repository import db_criar_sessao_banco, db_buscar_sessao_banco, db_deletar_sessao_banco
from app.repositories.unidade_saude_repository import db_buscar_unidade_saude_by_id

from app.security.criador_strings import criar_token_aleatorio
from app.security.hasher_sha256 import hashear_sha256

from datetime import datetime, timezone

from app.core import ADMIN_PASSWORD, SESSION_DURATION

security = HTTPBearer()


def obter_session_cookie(session_token: str | None = Cookie(default=None, alias="session")):
    return session_token

def verificar_credencial_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    credencial = credentials.credentials

    if credencial != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credencial inválida"
        )

    return True


def service_delete_current_unidade_saude(db: Session, response: Response, session_token: str | None = Depends(obter_session_cookie)):
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
    )
            
    token_hash = hashear_sha256(session_token)
    
    db_deletar_sessao_banco(db, token_hash)
    
    response.delete_cookie("session")
        
    return {
        "message": "Logout realizado com sucesso"
    }


def service_get_current_unidade_saude(db: Session, session_token: str | None = Depends(obter_session_cookie)) -> UnidadeSaude_Detailed_Response | None:
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    token_hash = hashear_sha256(session_token)
    
    sessao = db_buscar_sessao_banco(db, token_hash)
    
    if sessao is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    if sessao.expira_em < datetime.now(timezone.utc).replace(tzinfo=None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão expirada"
        )
        
    unidade_saude = db_buscar_unidade_saude_by_id(db, sessao.unidade_saude_id)
    
    if unidade_saude is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unidade de saúde não encontrada"
        )
    
    return unidade_saude
    

def service_fazer_login(db: Session, unidade_saude_login: UnidadeSaude_Login, response: Response):
    unidade_saude_id = service_buscar_unidade_saude_by_nome_login(db, unidade_saude_login)
    
    session_token = criar_token_aleatorio(32)
    session_token_hashed = hashear_sha256(session_token)
    
    db_criar_sessao_banco(db, session_token_hashed, unidade_saude_id)
    
    response.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=SESSION_DURATION
    )
    
    return {
        "message": "Login realizado com sucesso"
    }