from datetime import datetime
from pathlib import Path
from typing import Optional

from app.base_datos.conexion import obtener_conexion
from app.modelos.tarea import Tarea


class ServicioTareas:

    PRIORIDADES_VALIDAS = (
        "Baja",
        "Media",
        "Alta",
        "Urgente",
    )

    ESTADOS_VALIDOS = (
        "Pendiente",
        "En progreso",
        "Completada",
    )

    def __init__(
        self,
        ruta_base_datos: Path | None = None,
    ):
        self.ruta_base_datos = ruta_base_datos

    def crear_tarea(
        self,
        titulo: str,
        descripcion: str = "",
        prioridad: str = "Media",
        estado: str = "Pendiente",
        categoria: str = "General",
        fecha_limite: Optional[str] = None,
    ) -> Tarea:

        titulo = titulo.strip()
        descripcion = descripcion.strip()
        prioridad = prioridad.strip()
        estado = estado.strip()
        categoria = categoria.strip()

        if not titulo:
            raise ValueError(
                "El título de la tarea no puede estar vacío."
            )

        if not categoria:
            categoria = "General"

        self.validar_prioridad(prioridad)
        self.validar_estado(estado)

        fecha_limite = self.validar_fecha_limite(
            fecha_limite
        )

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            cursor = conexion.execute(
                """
                INSERT INTO tareas (
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                ),
            )

            conexion.commit()
            id_tarea = cursor.lastrowid

        tarea = self.obtener_tarea(id_tarea)

        if tarea is None:
            raise RuntimeError(
                "No se pudo crear la tarea."
            )

        return tarea

    def obtener_tareas(self) -> list[Tarea]:

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            filas = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    fecha_creacion
                FROM tareas
                ORDER BY id DESC
                """
            ).fetchall()

        return [
            self.convertir_fila_a_tarea(fila)
            for fila in filas
        ]

    def obtener_tarea(
        self,
        id_tarea: int,
    ) -> Optional[Tarea]:

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            fila = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    fecha_creacion
                FROM tareas
                WHERE id = ?
                """,
                (id_tarea,),
            ).fetchone()

        if fila is None:
            return None

        return self.convertir_fila_a_tarea(fila)

    def actualizar_tarea(
        self,
        id_tarea: int,
        titulo: str,
        descripcion: str,
        prioridad: str,
        estado: str,
        categoria: str,
        fecha_limite: Optional[str],
    ) -> bool:

        titulo = titulo.strip()
        descripcion = descripcion.strip()
        prioridad = prioridad.strip()
        estado = estado.strip()
        categoria = categoria.strip()

        if not titulo:
            raise ValueError(
                "El título de la tarea no puede estar vacío."
            )

        if not categoria:
            categoria = "General"

        self.validar_prioridad(prioridad)
        self.validar_estado(estado)

        fecha_limite = self.validar_fecha_limite(
            fecha_limite
        )

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            cursor = conexion.execute(
                """
                UPDATE tareas
                SET
                    titulo = ?,
                    descripcion = ?,
                    prioridad = ?,
                    estado = ?,
                    categoria = ?,
                    fecha_limite = ?
                WHERE id = ?
                """,
                (
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    id_tarea,
                ),
            )

            conexion.commit()

        return cursor.rowcount > 0

    def eliminar_tarea(
        self,
        id_tarea: int,
    ) -> bool:

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            cursor = conexion.execute(
                """
                DELETE FROM tareas
                WHERE id = ?
                """,
                (id_tarea,),
            )

            conexion.commit()

        return cursor.rowcount > 0

    def cambiar_estado(
        self,
        id_tarea: int,
        nuevo_estado: str,
    ) -> bool:

        self.validar_estado(nuevo_estado)

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            cursor = conexion.execute(
                """
                UPDATE tareas
                SET estado = ?
                WHERE id = ?
                """,
                (
                    nuevo_estado,
                    id_tarea,
                ),
            )

            conexion.commit()

        return cursor.rowcount > 0

    def buscar_tareas(
        self,
        texto: str,
    ) -> list[Tarea]:

        texto = texto.strip()

        if not texto:
            return self.obtener_tareas()

        patron = f"%{texto}%"

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            filas = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    fecha_creacion
                FROM tareas
                WHERE
                    titulo LIKE ?
                    OR descripcion LIKE ?
                    OR categoria LIKE ?
                ORDER BY id DESC
                """,
                (
                    patron,
                    patron,
                    patron,
                ),
            ).fetchall()

        return [
            self.convertir_fila_a_tarea(fila)
            for fila in filas
        ]

    def filtrar_por_estado(
        self,
        estado: str,
    ) -> list[Tarea]:

        self.validar_estado(estado)

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            filas = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    fecha_creacion
                FROM tareas
                WHERE estado = ?
                ORDER BY id DESC
                """,
                (estado,),
            ).fetchall()

        return [
            self.convertir_fila_a_tarea(fila)
            for fila in filas
        ]

    def filtrar_por_prioridad(
        self,
        prioridad: str,
    ) -> list[Tarea]:

        self.validar_prioridad(prioridad)

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            filas = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    fecha_creacion
                FROM tareas
                WHERE prioridad = ?
                ORDER BY id DESC
                """,
                (prioridad,),
            ).fetchall()

        return [
            self.convertir_fila_a_tarea(fila)
            for fila in filas
        ]

    def obtener_tareas_vencidas(
        self,
    ) -> list[Tarea]:

        fecha_actual = datetime.now().strftime(
            "%Y-%m-%d"
        )

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            filas = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    fecha_creacion
                FROM tareas
                WHERE
                    fecha_limite IS NOT NULL
                    AND fecha_limite < ?
                    AND estado != 'Completada'
                ORDER BY fecha_limite ASC
                """,
                (fecha_actual,),
            ).fetchall()

        return [
            self.convertir_fila_a_tarea(fila)
            for fila in filas
        ]

    def obtener_tareas_por_fecha(
        self,
    ) -> list[Tarea]:

        with obtener_conexion(
            self.ruta_base_datos
        ) as conexion:

            filas = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    prioridad,
                    estado,
                    categoria,
                    fecha_limite,
                    fecha_creacion
                FROM tareas
                ORDER BY
                    fecha_limite IS NULL,
                    fecha_limite ASC
                """
            ).fetchall()

        return [
            self.convertir_fila_a_tarea(fila)
            for fila in filas
        ]

    def validar_prioridad(
        self,
        prioridad: str,
    ) -> None:

        if prioridad not in self.PRIORIDADES_VALIDAS:
            raise ValueError(
                "La prioridad no es válida."
            )

    def validar_estado(
        self,
        estado: str,
    ) -> None:

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(
                "El estado no es válido."
            )

    def validar_fecha_limite(
        self,
        fecha_limite: Optional[str],
    ) -> Optional[str]:

        if not fecha_limite:
            return None

        fecha_limite = fecha_limite.strip()

        if not fecha_limite:
            return None

        try:
            datetime.strptime(
                fecha_limite,
                "%Y-%m-%d",
            )

        except ValueError as error:
            raise ValueError(
                "La fecha límite debe tener "
                "el formato AAAA-MM-DD."
            ) from error

        return fecha_limite

    def convertir_fila_a_tarea(
        self,
        fila,
    ) -> Tarea:

        return Tarea(
            id=fila["id"],
            titulo=fila["titulo"],
            descripcion=fila["descripcion"],
            prioridad=fila["prioridad"],
            estado=fila["estado"],
            categoria=fila["categoria"],
            fecha_limite=fila["fecha_limite"],
            fecha_creacion=fila["fecha_creacion"],
        )