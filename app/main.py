from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.unidade_saude import unidade_saude_router
from app.routers.auth import auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(unidade_saude_router)
app.include_router(auth_router)