from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from api.rotas_usuarios import usuario_publico
from controllers.usuario_controller import UsuarioController

router = APIRouter(
    prefix="/auth",
    tags=["autenticacao"]
)

controller = UsuarioController()


class Login(BaseModel):
    nome: str
    senha: str


@router.post("/login")
def login(dados: Login):
    resposta = controller.autenticar(dados.nome, dados.senha)

    if not resposta["sucesso"]:
        if resposta["tipo"] == "REGRA_NEGOCIO":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=resposta["mensagem"]
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=resposta["mensagem"]
        )

    dados = resposta["dados"]

    return {
        "dados": {
            "access_token": dados["access_token"],
            "token_type": dados["token_type"],
            "expires_in": dados["expires_in"],
            "usuario": usuario_publico(dados["usuario"])
        }
    }