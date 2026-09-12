from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_datos.base import Base


if TYPE_CHECKING:
    from app.modelos.tarea import Tarea
    from app.modelos.usuario import Usuario


class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "usuarios.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="proyectos"
    )

    tareas: Mapped[list["Tarea"]] = relationship(
        back_populates="proyecto"
    )