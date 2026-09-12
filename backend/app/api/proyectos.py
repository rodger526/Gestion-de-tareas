from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.base_datos.sesion import obtener_db
from app.core.dependencias import obtener_usuario_actual
from app.esquemas.proyecto import (
    ProyectoActualizar,
    ProyectoCrear,
    ProyectoRespuesta,
)
from app.modelos.proyecto import Proyecto
from app.modelos.usuario import Usuario


router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"],
)


def obtener_proyecto_usuario(
    proyecto_id: int,
    usuario_id: int,
    db: Session,
) -> Proyecto:

    proyecto = db.scalar(
        select(Proyecto).where(
            Proyecto.id == proyecto_id,
            Proyecto.usuario_id == usuario_id,
        )
    )

    if proyecto is None:
        raise HTTPException(
            status_code=404,
            detail="Proyecto no encontrado.",
        )

    return proyecto


@router.get(
    "",
    response_model=list[ProyectoRespuesta],
)
def listar(
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    return db.scalars(
        select(Proyecto)
        .where(
            Proyecto.usuario_id == usuario.id
        )
        .order_by(
            Proyecto.id.desc()
        )
    ).all()


@router.post(
    "",
    response_model=ProyectoRespuesta,
    status_code=201,
)
def crear(
    datos: ProyectoCrear,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    proyecto = Proyecto(
        nombre=datos.nombre.strip(),
        descripcion=datos.descripcion.strip(),
        usuario_id=usuario.id,
    )

    db.add(proyecto)
    db.commit()
    db.refresh(proyecto)

    return proyecto


@router.put(
    "/{proyecto_id}",
    response_model=ProyectoRespuesta,
)
def actualizar(
    proyecto_id: int,
    datos: ProyectoActualizar,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    proyecto = obtener_proyecto_usuario(
        proyecto_id,
        usuario.id,
        db,
    )

    proyecto.nombre = datos.nombre.strip()
    proyecto.descripcion = datos.descripcion.strip()

    db.commit()
    db.refresh(proyecto)

    return proyecto


@router.delete(
    "/{proyecto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(
    proyecto_id: int,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    proyecto = obtener_proyecto_usuario(
        proyecto_id,
        usuario.id,
        db,
    )

    db.delete(proyecto)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )