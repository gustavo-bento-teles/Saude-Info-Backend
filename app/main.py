from fastapi import FastAPI

from app.routers.admin import admin_router
from app.routers.login import login_router

app = FastAPI()

app.include_router(admin_router)
app.include_router(login_router)