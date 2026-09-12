from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.base_datos.conexion import (
    inicializar_base_datos,
)
from app.rutas.tareas import (
    router as tareas_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_base_datos()

    yield


app = FastAPI(
    title="Gestor de Tareas API",
    description=(
        "API REST para la gestión de tareas. "
        "Incluye prioridades, categorías, estados, "
        "fechas límite, filtros y paginación."
    ),
    version="4.2.0",
    lifespan=lifespan,
)


@app.get(
    "/",
    tags=["Sistema"],
)
def inicio():

    return {
        "nombre": "Gestor de Tareas API",
        "version": "4.2.0",
        "estado": "funcionando",
    }


@app.get(
    "/health",
    tags=["Sistema"],
)
def health():

    return {
        "status": "ok"
    }


app.include_router(
    tareas_router
)