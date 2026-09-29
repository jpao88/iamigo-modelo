from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from controllers.usuario_controller import UsuarioController
from core.seguranca import validar_token_acesso

bearer = HTTPBearer(auto_error=False)
controller = UsuarioController()


def _nao_autenticado(mensagem):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=mensagem,
        headers={"WWW-Authenticate": "Bearer"}
    )


def obter_usuario_autenticado(
    credenciais: Optional[HTTPAuthorizationCredentials] = Depends(bearer)
):
    if credenciais is None:
        raise _nao_autenticado("Token de acesso ausente.")

    try:
        usuario_id = validar_token_acesso(credenciais.credentials)
    except ValueError:
        raise _nao_autenticado("Token inválido ou expirado.")

    resposta = controller.buscar_perfil(usuario_id)

    if not resposta["sucesso"]:
        if resposta["tipo"] == "FALHA_TECNICA":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=resposta["mensagem"]
            )
        raise _nao_autenticado("Token inválido ou expirado.")

    return resposta["dados"]