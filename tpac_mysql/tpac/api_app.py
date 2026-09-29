import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.rotas_usuarios import router as usuarios_router
from api.rotas_tarefas import router as tarefas_router
from api.rotas_auth import router as auth_router

load_dotenv()

ORIGENS_PADRAO = (
    "http://localhost:5500,"
    "http://127.0.0.1:5500,"
    "http://localhost:5173,"
    "http://127.0.0.1:5173"
)

origens_permitidas = [
    origem.strip()
    for origem in os.getenv("CORS_ORIGINS", ORIGENS_PADRAO).split(",")
    if origem.strip()
]

app = FastAPI(
    title="TPaC API",
    description="API criada na Aula 05",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(usuarios_router)
app.include_router(tarefas_router)
app.include_router(auth_router)


@app.get("/")
def inicio():
    return {
        "sistema": "TPaC",
        "api": "funcionando"
    }