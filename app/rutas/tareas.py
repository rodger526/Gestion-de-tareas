from typing import Optional

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Response,
    status,
)

from app.esquemas.tarea import (
    CambioEstado,
    RespuestaPaginada,
    TareaActualizar,
    TareaCrear,
    TareaRespuesta,
)
from app.servicios.servicio_tareas import (
    ServicioTareas,
)


router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
)

servicio_tareas = ServicioTareas()


def convertir_tarea_respuesta(
    tarea,
) -> TareaRespuesta:

    return TareaRespuesta(
        id=tarea.id,
        titulo=tarea.titulo,
        descripcion=tarea.descripcion,
        prioridad=tarea.prioridad,
        estado=tarea.estado,
        categoria=tarea.categoria,
        fecha_limite=tarea.fecha_limite,
        fecha_creacion=(
            str(tarea.fecha_creacion)
            if tarea.fecha_creacion
            else None
        ),
    )


@router.get(
    "",
    response_model=RespuestaPaginada,
)
def listar_tareas(
    pagina: int = Query(
        default=1,
        ge=1,
    ),
    limite: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    estado: Optional[str] = None,
    prioridad: Optional[str] = None,
    categoria: Optional[str] = None,
    texto: Optional[str] = None,
):

    try:
        tareas, total = (
            servicio_tareas.obtener_tareas_filtradas(
                estado=estado,
                prioridad=prioridad,
                categoria=categoria,
                texto=texto,
                pagina=pagina,
                limite=limite,
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return RespuestaPaginada(
        total=total,
        pagina=pagina,
        limite=limite,
        tareas=[
            convertir_tarea_respuesta(
                tarea
            )
            for tarea in tareas
        ],
    )


@router.get(
    "/vencidas",
    response_model=list[TareaRespuesta],
)
def listar_tareas_vencidas():

    tareas = (
        servicio_tareas.obtener_tareas_vencidas()
    )

    return [
        convertir_tarea_respuesta(tarea)
        for tarea in tareas
    ]


@router.get(
    "/ordenadas-por-fecha",
    response_model=list[TareaRespuesta],
)
def listar_tareas_por_fecha():

    tareas = (
        servicio_tareas.obtener_tareas_por_fecha()
    )

    return [
        convertir_tarea_respuesta(tarea)
        for tarea in tareas
    ]


@router.get(
    "/{id_tarea}",
    response_model=TareaRespuesta,
)
def obtener_tarea(
    id_tarea: int,
):

    tarea = servicio_tareas.obtener_tarea(
        id_tarea
    )

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada.",
        )

    return convertir_tarea_respuesta(
        tarea
    )


@router.post(
    "",
    response_model=TareaRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_tarea(
    datos: TareaCrear,
):

    try:
        tarea = servicio_tareas.crear_tarea(
            titulo=datos.titulo,
            descripcion=datos.descripcion,
            prioridad=datos.prioridad,
            estado=datos.estado,
            categoria=datos.categoria,
            fecha_limite=datos.fecha_limite,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    return convertir_tarea_respuesta(
        tarea
    )


@router.put(
    "/{id_tarea}",
    response_model=TareaRespuesta,
)
def actualizar_tarea(
    id_tarea: int,
    datos: TareaActualizar,
):

    existente = servicio_tareas.obtener_tarea(
        id_tarea
    )

    if existente is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada.",
        )

    try:
        servicio_tareas.actualizar_tarea(
            id_tarea=id_tarea,
            titulo=datos.titulo,
            descripcion=datos.descripcion,
            prioridad=datos.prioridad,
            estado=datos.estado,
            categoria=datos.categoria,
            fecha_limite=datos.fecha_limite,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    tarea = servicio_tareas.obtener_tarea(
        id_tarea
    )

    return convertir_tarea_respuesta(
        tarea
    )


@router.patch(
    "/{id_tarea}/estado",
    response_model=TareaRespuesta,
)
def cambiar_estado(
    id_tarea: int,
    datos: CambioEstado,
):

    existente = servicio_tareas.obtener_tarea(
        id_tarea
    )

    if existente is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada.",
        )

    servicio_tareas.cambiar_estado(
        id_tarea=id_tarea,
        nuevo_estado=datos.estado,
    )

    actualizada = servicio_tareas.obtener_tarea(
        id_tarea
    )

    return convertir_tarea_respuesta(
        actualizada
    )


@router.delete(
    "/{id_tarea}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_tarea(
    id_tarea: int,
):

    existente = servicio_tareas.obtener_tarea(
        id_tarea
    )

    if existente is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada.",
        )

    servicio_tareas.eliminar_tarea(
        id_tarea
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )