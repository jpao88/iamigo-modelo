from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, String
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
    senha_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now())