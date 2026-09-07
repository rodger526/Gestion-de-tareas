from app.base_datos.conexion import inicializar_base_datos
from app.servicios.servicio_tareas import ServicioTareas


servicio_tareas = ServicioTareas()


def mostrar_encabezado() -> None:
    print()
    print("=" * 60)
    print("                  GESTOR DE TAREAS")
    print("=" * 60)


def mostrar_menu() -> None:
    print()
    print("1. Crear tarea")
    print("2. Ver tareas")
    print("3. Editar tarea")
    print("4. Cambiar estado")
    print("5. Eliminar tarea")
    print("6. Salir")
    print()


def seleccionar_prioridad(
    prioridad_actual: str = "Media",
) -> str:

    print("\nPrioridad:")
    print("1. Baja")
    print("2. Media")
    print("3. Alta")
    print("4. Urgente")

    opcion = input(
        f"Seleccione prioridad [{prioridad_actual}]: "
    ).strip()

    prioridades = {
        "1": "Baja",
        "2": "Media",
        "3": "Alta",
        "4": "Urgente",
    }

    if not opcion:
        return prioridad_actual

    return prioridades.get(
        opcion,
        prioridad_actual,
    )


def seleccionar_estado(
    estado_actual: str = "Pendiente",
) -> str:

    print("\nEstado:")
    print("1. Pendiente")
    print("2. En progreso")
    print("3. Completada")

    opcion = input(
        f"Seleccione estado [{estado_actual}]: "
    ).strip()

    estados = {
        "1": "Pendiente",
        "2": "En progreso",
        "3": "Completada",
    }

    if not opcion:
        return estado_actual

    return estados.get(
        opcion,
        estado_actual,
    )


def crear_tarea() -> None:
    print("\n--- Crear tarea ---")

    titulo = input("Título: ")
    descripcion = input("Descripción: ")

    prioridad = seleccionar_prioridad()

    fecha_limite = input(
        "Fecha límite (AAAA-MM-DD, opcional): "
    ).strip()

    try:
        tarea = servicio_tareas.crear_tarea(
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            estado="Pendiente",
            fecha_limite=fecha_limite,
        )

        print(
            f"\nTarea #{tarea.id} "
            "creada correctamente."
        )

    except ValueError as error:
        print(f"\nError: {error}")


def mostrar_tareas() -> None:
    tareas = servicio_tareas.obtener_tareas()

    print("\n--- Lista de tareas ---")

    if not tareas:
        print("No hay tareas registradas.")
        return

    for tarea in tareas:

        if tarea.estado == "Completada":
            simbolo = "✓"
        elif tarea.estado == "En progreso":
            simbolo = "→"
        else:
            simbolo = "○"

        print()
        print(
            f"{simbolo} [{tarea.id}] "
            f"{tarea.titulo}"
        )

        print(
            f"    Estado: {tarea.estado}"
        )

        print(
            f"    Prioridad: {tarea.prioridad}"
        )

        if tarea.descripcion:
            print(
                f"    Descripción: "
                f"{tarea.descripcion}"
            )

        if tarea.fecha_limite:
            print(
                f"    Fecha límite: "
                f"{tarea.fecha_limite}"
            )

    print()


def editar_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "ID de la tarea que desea editar: "
            )
        )

    except ValueError:
        print("El ID introducido no es válido.")
        return

    tarea = servicio_tareas.obtener_tarea(id_tarea)

    if tarea is None:
        print("No se encontró la tarea.")
        return

    print(
        "\nDeje un campo vacío para conservar "
        "su valor actual."
    )

    titulo = input(
        f"Título [{tarea.titulo}]: "
    ).strip()

    descripcion = input(
        f"Descripción [{tarea.descripcion}]: "
    ).strip()

    if not titulo:
        titulo = tarea.titulo

    if not descripcion:
        descripcion = tarea.descripcion

    prioridad = seleccionar_prioridad(
        tarea.prioridad
    )

    estado = seleccionar_estado(
        tarea.estado
    )

    fecha_limite = input(
        f"Fecha límite "
        f"[{tarea.fecha_limite or 'Sin fecha'}]: "
    ).strip()

    if not fecha_limite:
        fecha_limite = tarea.fecha_limite

    try:
        actualizada = servicio_tareas.actualizar_tarea(
            id_tarea=id_tarea,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            estado=estado,
            fecha_limite=fecha_limite,
        )

        if actualizada:
            print(
                "Tarea actualizada correctamente."
            )
        else:
            print(
                "No se pudo actualizar la tarea."
            )

    except ValueError as error:
        print(f"Error: {error}")


def cambiar_estado_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "ID de la tarea que desea modificar: "
            )
        )

    except ValueError:
        print("El ID introducido no es válido.")
        return

    tarea = servicio_tareas.obtener_tarea(id_tarea)

    if tarea is None:
        print("No se encontró la tarea.")
        return

    nuevo_estado = seleccionar_estado(
        tarea.estado
    )

    try:
        if servicio_tareas.cambiar_estado(
            id_tarea,
            nuevo_estado,
        ):
            print(
                f"Estado actualizado a "
                f'"{nuevo_estado}".'
            )
        else:
            print(
                "No se pudo actualizar el estado."
            )

    except ValueError as error:
        print(f"Error: {error}")


def eliminar_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "ID de la tarea que desea eliminar: "
            )
        )

    except ValueError:
        print("El ID introducido no es válido.")
        return

    tarea = servicio_tareas.obtener_tarea(id_tarea)

    if tarea is None:
        print("No se encontró la tarea.")
        return

    confirmacion = input(
        f'¿Desea eliminar "{tarea.titulo}"? '
        "(s/n): "
    ).strip().lower()

    if confirmacion != "s":
        print("Eliminación cancelada.")
        return

    if servicio_tareas.eliminar_tarea(id_tarea):
        print("Tarea eliminada correctamente.")
    else:
        print("No se pudo eliminar la tarea.")


def main() -> None:
    inicializar_base_datos()

    while True:
        mostrar_encabezado()
        mostrar_menu()

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        match opcion:

            case "1":
                crear_tarea()

            case "2":
                mostrar_tareas()

            case "3":
                editar_tarea()

            case "4":
                cambiar_estado_tarea()

            case "5":
                eliminar_tarea()

            case "6":
                print(
                    "\nGracias por utilizar "
                    "el Gestor de Tareas."
                )
                break

            case _:
                print(
                    "\nLa opción seleccionada "
                    "no es válida."
                )


if __name__ == "__main__":
    main()