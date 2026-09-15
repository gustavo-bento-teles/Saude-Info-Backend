from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response, Cookie, Header

from sqlalchemy.orm import Session
from app.schemas.unidade_saude_schema import UnidadeSaude_Login
from app.services.unidade_saude_service import service_buscar_unidade_saude_by_nome_login
from app.repositories.session_repository import db_criar_sessao_banco, db_buscar_sessao_banco, db_deletar_sessao_banco
from app.repositories.unidade_saude_repository import db_buscar_unidade_saude_by_id

from app.security.criador_strings import criar_token_aleatorio
from app.security.hasher_sha256 import hashear_sha256

from app.main import SessaoInvalidaException

from datetime import datetime, timezone

from app.core import ADMIN_PASSWORD, SESSION_DURATION

security = HTTPBearer()


def obter_csrf_token(csrf_token: str | None = Header(..., alias="X-CSRF-Token")):
    return csrf_token

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


def service_delete_current_unidade_saude(
    db: Session,
    response: Response,
    csrf_token: str | None,
    session_token: str | None
):
    
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    if csrf_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token inválido"
        )
            
    token_hash = hashear_sha256(session_token)
    csrf_token_hashed = hashear_sha256(csrf_token)
    
    sessao = db_buscar_sessao_banco(db, token_hash, csrf_token_hashed)
    
    if sessao is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sessão inválida"
        )
    
    db_deletar_sessao_banco(db, token_hash, csrf_token_hashed)
    
    response.delete_cookie("session", path="/")
    response.delete_cookie("csrf_token", path="/")
        
    return {
        "message": "Logout realizado com sucesso"
    }


def service_get_current_unidade_saude(
    db: Session,
    csrf_token: str | None,
    session_token: str | None
) -> int:
    
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    
    if csrf_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token inválido"
        )
        
    token_hash = hashear_sha256(session_token)
    csrf_token_hashed = hashear_sha256(csrf_token)
    
    sessao = db_buscar_sessao_banco(db, token_hash, csrf_token_hashed)
    
    if sessao is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
        
    if sessao.expira_em < datetime.now(timezone.utc).replace(tzinfo=None):
        db_deletar_sessao_banco(db, token_hash, csrf_token_hashed)
        raise SessaoInvalidaException()
        
    unidade_saude = db_buscar_unidade_saude_by_id(db, sessao.unidade_saude_id)
    
    if unidade_saude is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unidade de saúde não encontrada"
        )
    
    return unidade_saude.id
    

def service_fazer_login(
    db: Session,
    unidade_saude_login: UnidadeSaude_Login,
    response: Response
):
    
    unidade_saude_id = service_buscar_unidade_saude_by_nome_login(db, unidade_saude_login)
    
    session_token = criar_token_aleatorio(32)
    session_token_hashed = hashear_sha256(session_token)
    
    csrf_token = criar_token_aleatorio(32)
    csrf_token_hashed = hashear_sha256(csrf_token)
    
    db_criar_sessao_banco(db, csrf_token_hashed, session_token_hashed, unidade_saude_id)
    
    response.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        samesite="lax" ,
        path="/"
    )
    
    return {
        "message": "Login realizado com sucesso"
    }