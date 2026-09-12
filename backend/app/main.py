from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.autenticacion import (
    router as autenticacion_router,
)
from app.api.dashboard import (
    router as dashboard_router,
)
from app.api.proyectos import (
    router as proyectos_router,
)
from app.api.tareas import (
    router as tareas_router,
)
from app.core.config import configuracion


app = FastAPI(
    title="Gestor de Tareas API",
    version=configuracion.version,
    description=(
        "Backend para gestión de proyectos "
        "y tareas con autenticación JWT."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        configuracion.frontend_origin,
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "nombre": configuracion.nombre_app,
        "version": configuracion.version,
        "estado": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(
    autenticacion_router
)

app.include_router(
    proyectos_router
)

app.include_router(
    tareas_router
)

app.include_router(
    dashboard_router
)