import math

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.base_datos.sesion import obtener_db
from app.core.dependencias import obtener_usuario_actual
from app.esquemas.tarea import (
    CambioEstado,
    TareaActualizar,
    TareaCrear,
    TareaRespuesta,
    TareasPaginadas,
)
from app.modelos.proyecto import Proyecto
from app.modelos.tarea import Tarea
from app.modelos.usuario import Usuario


router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
)


def comprobar_proyecto(
    proyecto_id: int | None,
    usuario_id: int,
    db: Session,
) -> None:

    if proyecto_id is None:
        return

    proyecto = db.scalar(
        select(Proyecto).where(
            Proyecto.id == proyecto_id,
            Proyecto.usuario_id == usuario_id,
        )
    )

    if proyecto is None:
        raise HTTPException(
            status_code=400,
            detail="El proyecto no existe.",
        )


def obtener_tarea_usuario(
    tarea_id: int,
    usuario_id: int,
    db: Session,
) -> Tarea:

    tarea = db.scalar(
        select(Tarea).where(
            Tarea.id == tarea_id,
            Tarea.usuario_id == usuario_id,
        )
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada.",
        )

    return tarea


@router.get(
    "",
    response_model=TareasPaginadas,
)
def listar(
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    estado: str | None = None,
    prioridad: str | None = None,
    proyecto_id: int | None = None,
    buscar: str | None = None,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    condiciones = [
        Tarea.usuario_id == usuario.id
    ]

    if estado:
        condiciones.append(
            Tarea.estado == estado
        )

    if prioridad:
        condiciones.append(
            Tarea.prioridad == prioridad
        )

    if proyecto_id:
        condiciones.append(
            Tarea.proyecto_id == proyecto_id
        )

    if buscar:
        patron = f"%{buscar}%"

        condiciones.append(
            or_(
                Tarea.titulo.ilike(patron),
                Tarea.descripcion.ilike(patron),
                Tarea.categoria.ilike(patron),
            )
        )

    total = db.scalar(
        select(func.count())
        .select_from(Tarea)
        .where(*condiciones)
    ) or 0

    offset = (
        pagina - 1
    ) * limite

    tareas = db.scalars(
        select(Tarea)
        .where(*condiciones)
        .order_by(
            Tarea.fecha_creacion.desc()
        )
        .offset(offset)
        .limit(limite)
    ).all()

    paginas = (
        math.ceil(total / limite)
        if total > 0
        else 0
    )

    return {
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "paginas": paginas,
        "tareas": tareas,
    }


@router.get(
    "/{tarea_id}",
    response_model=TareaRespuesta,
)
def obtener(
    tarea_id: int,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    return obtener_tarea_usuario(
        tarea_id,
        usuario.id,
        db,
    )


@router.post(
    "",
    response_model=TareaRespuesta,
    status_code=201,
)
def crear(
    datos: TareaCrear,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    comprobar_proyecto(
        datos.proyecto_id,
        usuario.id,
        db,
    )

    tarea = Tarea(
        titulo=datos.titulo.strip(),
        descripcion=datos.descripcion.strip(),
        prioridad=datos.prioridad,
        estado=datos.estado,
        categoria=datos.categoria.strip(),
        fecha_limite=datos.fecha_limite,
        proyecto_id=datos.proyecto_id,
        usuario_id=usuario.id,
    )

    db.add(tarea)
    db.commit()
    db.refresh(tarea)

    return tarea


@router.put(
    "/{tarea_id}",
    response_model=TareaRespuesta,
)
def actualizar(
    tarea_id: int,
    datos: TareaActualizar,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    tarea = obtener_tarea_usuario(
        tarea_id,
        usuario.id,
        db,
    )

    comprobar_proyecto(
        datos.proyecto_id,
        usuario.id,
        db,
    )

    tarea.titulo = datos.titulo.strip()
    tarea.descripcion = datos.descripcion.strip()
    tarea.prioridad = datos.prioridad
    tarea.estado = datos.estado
    tarea.categoria = datos.categoria.strip()
    tarea.fecha_limite = datos.fecha_limite
    tarea.proyecto_id = datos.proyecto_id

    db.commit()
    db.refresh(tarea)

    return tarea


@router.patch(
    "/{tarea_id}/estado",
    response_model=TareaRespuesta,
)
def cambiar_estado(
    tarea_id: int,
    datos: CambioEstado,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    tarea = obtener_tarea_usuario(
        tarea_id,
        usuario.id,
        db,
    )

    tarea.estado = datos.estado

    db.commit()
    db.refresh(tarea)

    return tarea


@router.delete(
    "/{tarea_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(
    tarea_id: int,
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    tarea = obtener_tarea_usuario(
        tarea_id,
        usuario.id,
        db,
    )

    db.delete(tarea)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )