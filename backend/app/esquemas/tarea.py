from datetime import date, datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


Prioridad = Literal[
    "Baja",
    "Media",
    "Alta",
    "Urgente",
]

Estado = Literal[
    "Pendiente",
    "En progreso",
    "Completada",
]


class TareaCrear(BaseModel):
    titulo: str = Field(
        min_length=1,
        max_length=200,
    )

    descripcion: str = Field(
        default="",
        max_length=3000,
    )

    prioridad: Prioridad = "Media"

    estado: Estado = "Pendiente"

    categoria: str = Field(
        default="General",
        min_length=1,
        max_length=100,
    )

    fecha_limite: date | None = None

    proyecto_id: int | None = None


class TareaActualizar(TareaCrear):
    pass


class CambioEstado(BaseModel):
    estado: Estado


class TareaRespuesta(TareaCrear):
    id: int
    usuario_id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TareasPaginadas(BaseModel):
    total: int
    pagina: int
    limite: int
    paginas: int
    tareas: list[TareaRespuesta]