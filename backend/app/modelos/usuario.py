from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_datos.base import Base


if TYPE_CHECKING:
    from app.modelos.proyecto import Proyecto
    from app.modelos.tarea import Tarea


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    proyectos: Mapped[list["Proyecto"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    tareas: Mapped[list["Tarea"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
    )