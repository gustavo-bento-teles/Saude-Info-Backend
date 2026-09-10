from fastapi import APIRouter, status, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.auth_service import obter_session_cookie, obter_csrf_token

from app.schemas.medicamento_schema import Medicamento_Create

from app.services.medicamento_service import service_criar_medicamento

medicamento_router = APIRouter(
    prefix="/medicamento",
    tags=["Medicamento"]
)

@medicamento_router.post("/", status_code=status.HTTP_200_OK)
async def criar_medicamento(
    medicamento_create: Medicamento_Create,
    csrf_token: str | None = Depends(obter_csrf_token),
    session_cookie = Depends(obter_session_cookie),
    db: Session = Depends(get_db)
):
    return service_criar_medicamento(db, medicamento_create, csrf_token, session_cookie)