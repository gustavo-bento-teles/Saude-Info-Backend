from fastapi import FastAPI

from app.routers.admin import admin_router

app = FastAPI()

app.include_router(admin_router)