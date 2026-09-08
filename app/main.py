from fastapi import FastAPI

from app.routers.unidade_saude import admin_router

app = FastAPI()

app.include_router(admin_router)