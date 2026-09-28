from sqlalchemy import select

from config.database import SessionLocal
from models.passo import Passo


class PassoRepository:
    def listar_por_tarefa(self, tarefa_id):
        with SessionLocal() as session:
            comando = (
                select(Passo)
                .where(Passo.tarefa_id == tarefa_id)
                .order_by(Passo.ordem)
            )
            return list(session.scalars(comando))

    def criar_varios(self, tarefa_id, textos):
        with SessionLocal() as session:
            passos = [
                Passo(tarefa_id=tarefa_id, texto=texto, ordem=indice)
                for indice, texto in enumerate(textos, start=1)
            ]
            session.add_all(passos)
            session.commit()

            for passo in passos:
                session.refresh(passo)

            return passos

    def buscar_por_id(self, passo_id):
        with SessionLocal() as session:
            comando = select(Passo).where(Passo.id == passo_id)
            return session.scalar(comando)

    def alternar_concluido(self, passo_id):
        with SessionLocal() as session:
            comando = select(Passo).where(Passo.id == passo_id)
            passo = session.scalar(comando)
            passo.concluido = not passo.concluido
            session.commit()
            session.refresh(passo)
            return passo

    def excluir(self, passo_id):
        with SessionLocal() as session:
            comando = select(Passo).where(Passo.id == passo_id)
            passo = session.scalar(comando)
            session.delete(passo)
            session.commit()