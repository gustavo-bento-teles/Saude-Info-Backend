from fastapi import FastAPI

from app.routers.unidade_saude import unidade_saude_router

app = FastAPI()

app.include_router(unidade_saude_router)