from typing import Literal, Optional

from pydantic import BaseModel, Field


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


class TareaBase(BaseModel):
    titulo: str = Field(
        min_length=1,
        max_length=200,
    )

    descripcion: str = Field(
        default="",
        max_length=1000,
    )

    prioridad: Prioridad = "Media"
    estado: Estado = "Pendiente"

    categoria: str = Field(
        default="General",
        min_length=1,
        max_length=100,
    )

    fecha_limite: Optional[str] = None


class TareaCrear(TareaBase):
    pass


class TareaActualizar(TareaBase):
    pass


class CambioEstado(BaseModel):
    estado: Estado


class TareaRespuesta(TareaBase):
    id: int
    fecha_creacion: Optional[str] = None


class RespuestaPaginada(BaseModel):
    total: int
    pagina: int
    limite: int
    tareas: list[TareaRespuesta]