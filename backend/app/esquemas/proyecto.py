from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProyectoCrear(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=150,
    )

    descripcion: str = Field(
        default="",
        max_length=2000,
    )


class ProyectoActualizar(ProyectoCrear):
    pass


class ProyectoRespuesta(ProyectoCrear):
    id: int
    usuario_id: int
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )