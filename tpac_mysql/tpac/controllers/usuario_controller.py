import logging

from services.usuario_service import UsuarioService

logger = logging.getLogger("uvicorn.error")


class UsuarioController:
    def __init__(self, service=None):
        self.service = service or UsuarioService()

    def listar_perfis(self):
        return self.service.listar_usuarios()

    def criar_perfil(self, nome, estilo_instrucao):
        try:
            usuario = self.service.criar_usuario(nome, estilo_instrucao)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "mensagem": f"Perfil {usuario.nome} criado.",
                "dados": usuario
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em criar_perfil")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def atualizar_perfil(self, usuario_id, nome, estilo_instrucao):
        try:
            usuario = self.service.atualizar_usuario(usuario_id, nome, estilo_instrucao)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": usuario
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em atualizar_perfil")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def excluir_perfil(self, usuario_id):
        try:
            self.service.excluir_usuario(usuario_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO"
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em excluir_perfil")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def buscar_perfil(self, usuario_id):
        try:
            usuario = self.service.buscar_usuario(usuario_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": usuario
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em buscar_perfil")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def interpretar_mensagem(self, usuario_id, texto):
        try:
            resultado = self.service.interpretar_mensagem(usuario_id, texto)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": resultado
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em interpretar_mensagem")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def responder_pergunta(self, usuario_id, pergunta):
        try:
            linhas = self.service.responder_pergunta(usuario_id, pergunta)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": linhas
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except RuntimeError as erro:
            return {
                "sucesso": False,
                "tipo": "FALHA_IA",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em responder_pergunta")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def avancar_conversa(self, usuario_id, mensagem, estado=None, tarefa_parcial=None):
        try:
            resultado = self.service.avancar_conversa(
                usuario_id, mensagem, estado, tarefa_parcial
            )
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": resultado
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em avancar_conversa")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }