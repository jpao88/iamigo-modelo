from sqlalchemy import select

from config.database import SessionLocal
from models.tarefa import Tarefa


class TarefaRepository:
    def listar_por_usuario(self, usuario_id):
        with SessionLocal() as session:
            comando = (
                select(Tarefa)
                .where(Tarefa.usuario_id == usuario_id)
                .order_by(Tarefa.id)
            )
            return list(session.scalars(comando))

    def criar(self, usuario_id, tipo, titulo, descricao=None, prioridade="media", prazo=None):
        with SessionLocal() as session:
            tarefa = Tarefa(
                usuario_id=usuario_id,
                tipo=tipo,
                titulo=titulo,
                descricao=descricao,
                prioridade=prioridade,
                prazo=prazo
            )
            session.add(tarefa)
            session.commit()
            session.refresh(tarefa)
            return tarefa

    def buscar_por_id(self, tarefa_id):
        with SessionLocal() as session:
            comando = select(Tarefa).where(Tarefa.id == tarefa_id)
            return session.scalar(comando)

    def alternar_concluida(self, tarefa_id):
        with SessionLocal() as session:
            comando = select(Tarefa).where(Tarefa.id == tarefa_id)
            tarefa = session.scalar(comando)
            tarefa.concluida = not tarefa.concluida
            session.commit()
            session.refresh(tarefa)
            return tarefa

    def atualizar(self, tarefa_id, tipo, titulo, descricao, prioridade, prazo):
        with SessionLocal() as session:
            comando = select(Tarefa).where(Tarefa.id == tarefa_id)
            tarefa = session.scalar(comando)
            tarefa.tipo = tipo
            tarefa.titulo = titulo
            tarefa.descricao = descricao
            tarefa.prioridade = prioridade
            tarefa.prazo = prazo
            session.commit()
            session.refresh(tarefa)
            return tarefa

    def excluir(self, tarefa_id):
        with SessionLocal() as session:
            comando = select(Tarefa).where(Tarefa.id == tarefa_id)
            tarefa = session.scalar(comando)
            session.delete(tarefa)
            session.commit()