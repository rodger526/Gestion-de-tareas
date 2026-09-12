from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.base_datos.sesion import obtener_db
from app.core.dependencias import obtener_usuario_actual
from app.modelos.tarea import Tarea
from app.modelos.usuario import Usuario


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/resumen")
def resumen(
    db: Session = Depends(obtener_db),
    usuario: Usuario = Depends(
        obtener_usuario_actual
    ),
):

    def contar_por_estado(
        estado: str,
    ) -> int:

        return db.scalar(
            select(func.count())
            .select_from(Tarea)
            .where(
                Tarea.usuario_id == usuario.id,
                Tarea.estado == estado,
            )
        ) or 0

    total = db.scalar(
        select(func.count())
        .select_from(Tarea)
        .where(
            Tarea.usuario_id == usuario.id
        )
    ) or 0

    vencidas = db.scalar(
        select(func.count())
        .select_from(Tarea)
        .where(
            Tarea.usuario_id == usuario.id,
            Tarea.fecha_limite < date.today(),
            Tarea.estado != "Completada",
        )
    ) or 0

    return {
        "total": total,
        "pendientes": contar_por_estado(
            "Pendiente"
        ),
        "en_progreso": contar_por_estado(
            "En progreso"
        ),
        "completadas": contar_por_estado(
            "Completada"
        ),
        "vencidas": vencidas,
    }