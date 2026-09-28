from repositories.usuario_repository import UsuarioRepository
from core.interpretador import interpretar_mensagem as interpretar_texto
from core.ia_service import obter_resposta_ia
from core.conversa import ConversaTarefa, ESPERANDO_PRAZO, ESPERANDO_PRIORIDADE
from services.tarefa_service import TarefaService


class UsuarioService:
    def __init__(self, repository=None):
        self.repository = repository or UsuarioRepository()

    def listar_usuarios(self):
        return self.repository.listar()

    def buscar_usuario(self, usuario_id):
        usuario = self.repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        return usuario

    def criar_usuario(self, nome, estilo_instrucao):
        nome = nome.strip()

        if not nome:
            raise ValueError("O nome não pode ficar vazio.")

        if len(nome) < 3:
            raise ValueError("O nome precisa ter pelo menos 3 caracteres.")

        if estilo_instrucao not in {"direto", "detalhado"}:
            raise ValueError(
                "O estilo deve ser 'direto' ou 'detalhado'."
            )

        existente = self.repository.buscar_por_nome(nome)
        if existente is not None:
            raise ValueError("Já existe um perfil com esse nome.")

        return self.repository.criar(nome, estilo_instrucao)

    def atualizar_usuario(self, usuario_id, nome, estilo_instrucao):
        usuario = self.repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        nome = nome.strip()

        if not nome:
            raise ValueError("O nome não pode ficar vazio.")

        if len(nome) < 3:
            raise ValueError("O nome precisa ter pelo menos 3 caracteres.")

        if estilo_instrucao not in {"direto", "detalhado"}:
            raise ValueError(
                "O estilo deve ser 'direto' ou 'detalhado'."
            )

        existente = self.repository.buscar_por_nome(nome)
        if existente is not None and existente.id != usuario_id:
            raise ValueError("Já existe um perfil com esse nome.")

        return self.repository.atualizar(usuario_id, nome, estilo_instrucao)

    def excluir_usuario(self, usuario_id):
        usuario = self.repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        self.repository.excluir(usuario_id)

    def interpretar_mensagem(self, usuario_id, texto):
        usuario = self.repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        return interpretar_texto(texto)

    def responder_pergunta(self, usuario_id, pergunta):
        usuario = self.repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        linhas = obter_resposta_ia(pergunta, usuario.estilo_instrucao)

        if linhas and linhas[0].startswith("Erro"):
            raise RuntimeError(linhas[0])

        return linhas

    def avancar_conversa(self, usuario_id, mensagem, estado=None, tarefa_parcial=None):
        usuario = self.repository.buscar_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        estados_validos = {None, ESPERANDO_PRAZO, ESPERANDO_PRIORIDADE}

        if estado not in estados_validos:
            raise ValueError("Estado de conversa inválido.")

        tarefa_service = TarefaService()

        def persistir_na_api(categoria, titulo, prioridade, prazo):
            tarefa_service.criar_tarefa(
                usuario_id, categoria, titulo,
                prioridade=prioridade, prazo=prazo
            )

        conversa = ConversaTarefa(
            estado=estado,
            tarefa=tarefa_parcial,
            persistir_tarefa=persistir_na_api
        )

        if estado is None:
            interpretacao = interpretar_texto(mensagem)

            if interpretacao["intencao"] != "registrar_tarefa":
                raise ValueError(
                    "Não consegui identificar uma tarefa nessa mensagem."
                )

            respostas = conversa.iniciar(
                interpretacao["titulo"], interpretacao["categoria"]
            )
        else:
            respostas = conversa.processar(mensagem)

        return {
            "respostas": respostas,
            "estado": conversa.estado,
            "tarefa": conversa.tarefa
        }