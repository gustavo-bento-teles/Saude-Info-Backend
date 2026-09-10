from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from datetime import datetime, timedelta, timezone

from app.models.session import Session as TableSession

from app.core import SESSION_DURATION

def db_criar_sessao_banco(
    db: Session,
    csrf_token: str,
    session_token_hash: str,
    unidade_saude_id: int,
):
    tempo_expiracao = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=SESSION_DURATION)
    
    sessao: TableSession = TableSession(
        token_hash=session_token_hash,
        csrf_token=csrf_token,
        unidade_saude_id=unidade_saude_id,
        expira_em=tempo_expiracao
    )
    
    db.add(sessao)
    db.commit()
    

def db_buscar_sessao_banco(
    db: Session,
    session_token_hash: str,
    csrf_token: str
) -> TableSession | None:
    sessao = db.execute(
        select(TableSession)
            .where(
                TableSession.token_hash == session_token_hash,
                TableSession.csrf_token == csrf_token
            )
    ).scalar_one_or_none()
    
    return sessao if sessao is not None else None


def db_deletar_sessao_banco(
    db: Session,
    session_token_hash: str,
    csrf_token: str
):
    db.execute(
        delete(TableSession)
            .where(
                TableSession.token_hash == session_token_hash,
                TableSession.csrf_token == csrf_token
            )
    )
    
    db.commit()