from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_datos.base import Base


if TYPE_CHECKING:
    from app.modelos.proyecto import Proyecto
    from app.modelos.usuario import Usuario


class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    prioridad: Mapped[str] = mapped_column(
        String(20),
        default="Media",
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        default="Pendiente",
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(100),
        default="General",
        nullable=False,
    )

    fecha_limite: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "usuarios.id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )

    proyecto_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "proyectos.id",
            ondelete="SET NULL",
        ),
        index=True,
        nullable=True,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="tareas"
    )

    proyecto: Mapped["Proyecto | None"] = relationship(
        back_populates="tareas"
    )