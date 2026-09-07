import sqlite3
from pathlib import Path


DIRECTORIO_RAIZ = Path(__file__).resolve().parent.parent.parent
DIRECTORIO_DATOS = DIRECTORIO_RAIZ / "datos"
RUTA_BASE_DATOS = DIRECTORIO_DATOS / "gestor_tareas.db"


def obtener_conexion() -> sqlite3.Connection:
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    """

    DIRECTORIO_DATOS.mkdir(exist_ok=True)

    conexion = sqlite3.connect(RUTA_BASE_DATOS)

    # Permite acceder a las columnas por nombre.
    # Ejemplo: fila["titulo"]
    conexion.row_factory = sqlite3.Row

    return conexion


def inicializar_base_datos() -> None:
    """
    Crea las tablas necesarias si todavía no existen.
    """

    with obtener_conexion() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                completada INTEGER NOT NULL DEFAULT 0,
                fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conexion.commit()