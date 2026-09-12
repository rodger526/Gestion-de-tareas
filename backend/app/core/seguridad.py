from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import configuracion


password_hash = PasswordHash.recommended()


def crear_hash_password(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(
    password: str,
    hash_guardado: str,
) -> bool:
    return password_hash.verify(
        password,
        hash_guardado,
    )


def crear_token_acceso(
    usuario_id: int,
) -> str:

    expiracion = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=configuracion.minutos_token
        )
    )

    payload = {
        "sub": str(usuario_id),
        "exp": expiracion,
    }

    return jwt.encode(
        payload,
        configuracion.secret_key,
        algorithm=configuracion.algoritmo,
    )


def decodificar_token(
    token: str,
) -> int | None:

    try:
        payload = jwt.decode(
            token,
            configuracion.secret_key,
            algorithms=[
                configuracion.algoritmo
            ],
        )

        return int(payload["sub"])

    except (
        jwt.InvalidTokenError,
        KeyError,
        ValueError,
    ):
        return None