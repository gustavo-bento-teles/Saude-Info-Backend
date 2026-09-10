from fastapi import APIRouter, status, Depends, Response

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.unidade_saude_schema import UnidadeSaude_Login

from app.services.auth_service import service_fazer_login, service_delete_current_unidade_saude, obter_session_cookie

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def fazer_login(
    unidade_saude_login: UnidadeSaude_Login,
    response: Response,
    db: Session = Depends(get_db)
):
    return service_fazer_login(db, unidade_saude_login, response)

@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def fazer_logout(
    response: Response,
    csrf_token: str,
    db: Session = Depends(get_db),
    session_cookie = Depends(obter_session_cookie)
):
    return service_delete_current_unidade_saude(db, response, csrf_token, session_cookie)