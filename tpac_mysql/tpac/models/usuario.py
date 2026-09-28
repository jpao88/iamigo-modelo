from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from config.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True, nullable=False)
    estilo_instrucao: Mapped[str] = mapped_column(
        Enum("direto", "detalhado", name="estilo_instrucao_enum"),
        nullable=False,
        default="direto",
    )
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now())