import sqlite3
from pathlib import Path


DIRECTORIO_RAIZ = Path(__file__).resolve().parent.parent.parent
DIRECTORIO_DATOS = DIRECTORIO_RAIZ / "datos"

RUTA_BASE_DATOS = DIRECTORIO_DATOS / "gestor_tareas.db"


def obtener_conexion(
    ruta_base_datos: Path | None = None,
) -> sqlite3.Connection:
    """
    Crea y devuelve una conexión SQLite.
    """

    DIRECTORIO_DATOS.mkdir(exist_ok=True)

    ruta = ruta_base_datos or RUTA_BASE_DATOS

    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row

    return conexion


def columna_existe(
    conexion: sqlite3.Connection,
    tabla: str,
    columna: str,
) -> bool:
    columnas = conexion.execute(
        f"PRAGMA table_info({tabla})"
    ).fetchall()

    return any(
        fila["name"] == columna
        for fila in columnas
    )


def inicializar_base_datos(
    ruta_base_datos: Path | None = None,
) -> None:
    """
    Inicializa la base de datos indicada.

    Si no se proporciona una ruta, utiliza
    la base de datos principal.
    """

    with obtener_conexion(ruta_base_datos) as conexion:

        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                prioridad TEXT NOT NULL DEFAULT 'Media',
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                categoria TEXT NOT NULL DEFAULT 'General',
                fecha_limite TEXT,
                fecha_creacion TIMESTAMP NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        if not columna_existe(
            conexion,
            "tareas",
            "prioridad",
        ):
            conexion.execute(
                """
                ALTER TABLE tareas
                ADD COLUMN prioridad TEXT
                NOT NULL DEFAULT 'Media'
                """
            )

        if not columna_existe(
            conexion,
            "tareas",
            "estado",
        ):
            conexion.execute(
                """
                ALTER TABLE tareas
                ADD COLUMN estado TEXT
                NOT NULL DEFAULT 'Pendiente'
                """
            )

        if not columna_existe(
            conexion,
            "tareas",
            "categoria",
        ):
            conexion.execute(
                """
                ALTER TABLE tareas
                ADD COLUMN categoria TEXT
                NOT NULL DEFAULT 'General'
                """
            )

        if not columna_existe(
            conexion,
            "tareas",
            "fecha_limite",
        ):
            conexion.execute(
                """
                ALTER TABLE tareas
                ADD COLUMN fecha_limite TEXT
                """
            )

        conexion.commit()