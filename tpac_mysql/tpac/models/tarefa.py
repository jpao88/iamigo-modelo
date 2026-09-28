from datetime import date, datetime
from typing import Optional

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from config.database import Base


class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(
        Enum("tarefas_diarias", "tarefas_educacionais", name="tipo_tarefa_enum"),
        nullable=False,
    )
    titulo: Mapped[str] = mapped_column(nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(nullable=True)
    prioridade: Mapped[str] = mapped_column(
        Enum("baixa", "media", "alta", name="prioridade_enum"),
        nullable=False,
        default="media",
    )
    prazo: Mapped[Optional[date]] = mapped_column(nullable=True)
    concluida: Mapped[bool] = mapped_column(nullable=False, default=False)
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now())