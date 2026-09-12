from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tarea:
    id: Optional[int]
    titulo: str
    descripcion: str = ""
    prioridad: str = "Media"
    estado: str = "Pendiente"
    categoria: str = "General"
    fecha_limite: Optional[str] = None
    fecha_creacion: Optional[datetime] = None