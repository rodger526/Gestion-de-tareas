from typing import Optional

from app.base_datos.conexion import obtener_conexion
from app.modelos.tarea import Tarea


class ServicioTareas:
    """
    Contiene la lógica relacionada con la gestión de tareas.
    """

    def crear_tarea(
        self,
        titulo: str,
        descripcion: str = "",
    ) -> Tarea:

        titulo = titulo.strip()
        descripcion = descripcion.strip()

        if not titulo:
            raise ValueError(
                "El título de la tarea no puede estar vacío."
            )

        with obtener_conexion() as conexion:
            cursor = conexion.execute(
                """
                INSERT INTO tareas (
                    titulo,
                    descripcion
                )
                VALUES (?, ?)
                """,
                (
                    titulo,
                    descripcion,
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
        """
        Obtiene todas las tareas almacenadas.
        """

        with obtener_conexion() as conexion:
            filas = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    completada,
                    fecha_creacion
                FROM tareas
                ORDER BY id DESC
                """
            ).fetchall()

        return [
            Tarea(
                id=fila["id"],
                titulo=fila["titulo"],
                descripcion=fila["descripcion"],
                completada=bool(fila["completada"]),
                fecha_creacion=fila["fecha_creacion"],
            )
            for fila in filas
        ]

    def obtener_tarea(
        self,
        id_tarea: int,
    ) -> Optional[Tarea]:
        """
        Busca una tarea mediante su identificador.
        """

        with obtener_conexion() as conexion:
            fila = conexion.execute(
                """
                SELECT
                    id,
                    titulo,
                    descripcion,
                    completada,
                    fecha_creacion
                FROM tareas
                WHERE id = ?
                """,
                (id_tarea,),
            ).fetchone()

        if fila is None:
            return None

        return Tarea(
            id=fila["id"],
            titulo=fila["titulo"],
            descripcion=fila["descripcion"],
            completada=bool(fila["completada"]),
            fecha_creacion=fila["fecha_creacion"],
        )

    def actualizar_tarea(
        self,
        id_tarea: int,
        titulo: str,
        descripcion: str,
    ) -> bool:
        """
        Actualiza el título y descripción de una tarea.
        """

        titulo = titulo.strip()
        descripcion = descripcion.strip()

        if not titulo:
            raise ValueError(
                "El título de la tarea no puede estar vacío."
            )

        with obtener_conexion() as conexion:
            cursor = conexion.execute(
                """
                UPDATE tareas
                SET
                    titulo = ?,
                    descripcion = ?
                WHERE id = ?
                """,
                (
                    titulo,
                    descripcion,
                    id_tarea,
                ),
            )

            conexion.commit()

        return cursor.rowcount > 0

    def eliminar_tarea(
        self,
        id_tarea: int,
    ) -> bool:
        """
        Elimina una tarea mediante su identificador.
        """

        with obtener_conexion() as conexion:
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
    ) -> bool:
        """
        Cambia una tarea entre pendiente y completada.
        """

        tarea = self.obtener_tarea(id_tarea)

        if tarea is None:
            return False

        nuevo_estado = not tarea.completada

        with obtener_conexion() as conexion:
            conexion.execute(
                """
                UPDATE tareas
                SET completada = ?
                WHERE id = ?
                """,
                (
                    int(nuevo_estado),
                    id_tarea,
                ),
            )

            conexion.commit()

        return True