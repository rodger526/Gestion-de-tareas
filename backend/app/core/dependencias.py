from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.base_datos.sesion import obtener_db
from app.core.seguridad import decodificar_token
from app.modelos.usuario import Usuario


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(obtener_db),
) -> Usuario:

    usuario_id = decodificar_token(token)

    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    usuario = db.get(
        Usuario,
        usuario_id,
    )

    if usuario is None or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado.",
        )

    return usuario