from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.base_datos.sesion import obtener_db
from app.core.dependencias import obtener_usuario_actual
from app.core.seguridad import (
    crear_hash_password,
    crear_token_acceso,
    verificar_password,
)
from app.esquemas.autenticacion import (
    RegistroUsuario,
    TokenRespuesta,
    UsuarioRespuesta,
)
from app.modelos.usuario import Usuario


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


@router.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar(
    datos: RegistroUsuario,
    db: Session = Depends(obtener_db),
):

    existente = db.scalar(
        select(Usuario).where(
            Usuario.email == datos.email.lower()
        )
    )

    if existente:
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado.",
        )

    usuario = Usuario(
        nombre=datos.nombre.strip(),
        email=datos.email.lower(),
        password_hash=crear_hash_password(
            datos.password
        ),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@router.post(
    "/login",
    response_model=TokenRespuesta,
)
def login(
    formulario: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(obtener_db),
):

    usuario = db.scalar(
        select(Usuario).where(
            Usuario.email
            == formulario.username.lower()
        )
    )

    if (
        usuario is None
        or not verificar_password(
            formulario.password,
            usuario.password_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    token = crear_token_acceso(
        usuario.id
    )

    return TokenRespuesta(
        access_token=token
    )


@router.get(
    "/me",
    response_model=UsuarioRespuesta,
)
def perfil(
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):
    return usuario