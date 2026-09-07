from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tarea:
    id: Optional[int]
    titulo: str
    descripcion: str = ""
    completada: bool = False
    fecha_creacion: Optional[datetime] = None