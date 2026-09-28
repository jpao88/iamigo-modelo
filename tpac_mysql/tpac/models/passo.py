from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Passo(Base):
    __tablename__ = "passos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tarefa_id: Mapped[int] = mapped_column(ForeignKey("tarefas.id"), nullable=False)
    texto: Mapped[str] = mapped_column(nullable=False)
    concluido: Mapped[bool] = mapped_column(nullable=False, default=False)
    ordem: Mapped[int] = mapped_column(nullable=False, default=1)