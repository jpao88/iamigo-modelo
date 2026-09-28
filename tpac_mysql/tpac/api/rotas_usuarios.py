from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from controllers.usuario_controller import UsuarioController

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

controller = UsuarioController()


class NovoUsuario(BaseModel):
    nome: str
    estilo_instrucao: str = "direto"


class AtualizarUsuario(BaseModel):
    nome: str
    estilo_instrucao: str


class Mensagem(BaseModel):
    texto: str


class Pergunta(BaseModel):
    texto: str


class MensagemConversa(BaseModel):
    mensagem: str
    estado: Optional[str] = None
    tarefa_parcial: Optional[dict] = None


@router.get("")
def listar_usuarios():
    return {
        "dados": controller.listar_perfis()
    }


@router.get("/{usuario_id}")
def buscar_usuario(usuario_id: int):
    resposta = controller.buscar_perfil(usuario_id)

    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=404,
            detail=resposta["mensagem"]
        )

    return {
        "dados": resposta["dados"]
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: NovoUsuario):
    resposta = controller.criar_perfil(
        dados.nome,
        dados.estilo_instrucao
    )

    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=422,
            detail=resposta["mensagem"]
        )

    return {
        "dados": resposta["dados"]
    }


@router.put("/{usuario_id}")
def atualizar_usuario(usuario_id: int, dados: AtualizarUsuario):
    resposta = controller.atualizar_perfil(
        usuario_id, dados.nome, dados.estilo_instrucao
    )

    if not resposta["sucesso"]:
        status_code = 404 if resposta["mensagem"] == "Usuário não encontrado." else 422
        raise HTTPException(
            status_code=status_code,
            detail=resposta["mensagem"]
        )

    return {
        "dados": resposta["dados"]
    }


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_usuario(usuario_id: int):
    resposta = controller.excluir_perfil(usuario_id)

    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=404,
            detail=resposta["mensagem"]
        )


@router.post("/{usuario_id}/mensagens")
def interpretar_mensagem(usuario_id: int, dados: Mensagem):
    resposta = controller.interpretar_mensagem(usuario_id, dados.texto)

    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=404,
            detail=resposta["mensagem"]
        )

    return {
        "dados": resposta["dados"]
    }


@router.post("/{usuario_id}/perguntas")
def responder_pergunta(usuario_id: int, dados: Pergunta):
    resposta = controller.responder_pergunta(usuario_id, dados.texto)

    if not resposta["sucesso"]:
        status_code = 503 if resposta["tipo"] == "FALHA_IA" else 404
        raise HTTPException(
            status_code=status_code,
            detail=resposta["mensagem"]
        )

    return {
        "dados": resposta["dados"]
    }


@router.post("/{usuario_id}/conversa")
def avancar_conversa(usuario_id: int, dados: MensagemConversa):
    resposta = controller.avancar_conversa(
        usuario_id, dados.mensagem, dados.estado, dados.tarefa_parcial
    )

    if not resposta["sucesso"]:
        status_code = 404 if resposta["mensagem"] == "Usuário não encontrado." else 422
        raise HTTPException(
            status_code=status_code,
            detail=resposta["mensagem"]
        )

    return {
        "dados": resposta["dados"]
    }