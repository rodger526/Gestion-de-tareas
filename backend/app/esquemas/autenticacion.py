from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class RegistroUsuario(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"