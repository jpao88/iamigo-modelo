import logging

from services.tarefa_service import TarefaService

logger = logging.getLogger("uvicorn.error")


class TarefaController:
    def __init__(self, service=None):
        self.service = service or TarefaService()

    def listar_tarefas(self, usuario_id):
        try:
            tarefas = self.service.listar_tarefas(usuario_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": tarefas
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em listar_tarefas")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def criar_tarefa(self, usuario_id, tipo, titulo, descricao=None, prioridade="media", prazo=None):
        try:
            tarefa = self.service.criar_tarefa(
                usuario_id, tipo, titulo, descricao, prioridade, prazo
            )
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": tarefa
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em criar_tarefa")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def alternar_status(self, usuario_id, tarefa_id):
        try:
            tarefa = self.service.alternar_status(usuario_id, tarefa_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": tarefa
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em alternar_status")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def listar_passos(self, usuario_id, tarefa_id):
        try:
            passos = self.service.listar_passos(usuario_id, tarefa_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": passos
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em listar_passos")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def gerar_passos(self, usuario_id, tarefa_id):
        try:
            passos = self.service.gerar_passos(usuario_id, tarefa_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": passos
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
            logger.exception("Falha técnica em gerar_passos")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def alternar_status_passo(self, usuario_id, tarefa_id, passo_id):
        try:
            passo = self.service.alternar_status_passo(usuario_id, tarefa_id, passo_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": passo
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em alternar_status_passo")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def excluir_passo(self, usuario_id, tarefa_id, passo_id):
        try:
            self.service.excluir_passo(usuario_id, tarefa_id, passo_id)
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
            logger.exception("Falha técnica em excluir_passo")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }
    
    def buscar_tarefa(self, usuario_id, tarefa_id):
        try:
            tarefa = self.service.buscar_tarefa(usuario_id, tarefa_id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": tarefa
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em buscar_tarefa")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def atualizar_tarefa(self, usuario_id, tarefa_id, tipo, titulo, descricao=None, prioridade="media", prazo=None):
        try:
            tarefa = self.service.atualizar_tarefa(
                usuario_id, tarefa_id, tipo, titulo, descricao, prioridade, prazo
            )
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "dados": tarefa
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            logger.exception("Falha técnica em atualizar_tarefa")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def excluir_tarefa(self, usuario_id, tarefa_id):
        try:
            self.service.excluir_tarefa(usuario_id, tarefa_id)
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
            logger.exception("Falha técnica em excluir_tarefa")
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }