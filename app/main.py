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
    print("6. Buscar tareas")
    print("7. Filtrar tareas")
    print("8. Ver tareas vencidas")
    print("9. Ordenar por fecha límite")
    print("0. Salir")
    print()


def seleccionar_prioridad(
    prioridad_actual: str = "Media",
) -> str:
    print()
    print("Prioridad:")
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

    if opcion not in prioridades:
        print(
            "Opción no válida. "
            f"Se conservará '{prioridad_actual}'."
        )
        return prioridad_actual

    return prioridades[opcion]


def seleccionar_estado(
    estado_actual: str = "Pendiente",
) -> str:
    print()
    print("Estado:")
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

    if opcion not in estados:
        print(
            "Opción no válida. "
            f"Se conservará '{estado_actual}'."
        )
        return estado_actual

    return estados[opcion]


def mostrar_lista(
    tareas,
    titulo: str = "Tareas",
) -> None:
    print()
    print(f"--- {titulo} ---")

    if not tareas:
        print("No se encontraron tareas.")
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

        print(
            f"    Categoría: {tarea.categoria}"
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

        else:
            print(
                "    Fecha límite: Sin fecha"
            )


def crear_tarea() -> None:
    print()
    print("--- Crear tarea ---")

    titulo = input(
        "Título: "
    )

    descripcion = input(
        "Descripción: "
    )

    categoria = input(
        "Categoría [General]: "
    ).strip()

    if not categoria:
        categoria = "General"

    prioridad = seleccionar_prioridad()

    fecha_limite = input(
        "Fecha límite "
        "(AAAA-MM-DD, opcional): "
    ).strip()

    try:
        tarea = servicio_tareas.crear_tarea(
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            estado="Pendiente",
            categoria=categoria,
            fecha_limite=fecha_limite,
        )

        print()
        print(
            f"Tarea #{tarea.id} "
            "creada correctamente."
        )

    except ValueError as error:
        print()
        print(
            f"Error: {error}"
        )


def mostrar_tareas() -> None:
    tareas = servicio_tareas.obtener_tareas()

    mostrar_lista(
        tareas,
        "Lista de tareas",
    )


def editar_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "\nID de la tarea "
                "que desea editar: "
            )
        )

    except ValueError:
        print(
            "El ID introducido "
            "no es válido."
        )
        return

    tarea = servicio_tareas.obtener_tarea(
        id_tarea
    )

    if tarea is None:
        print(
            "No se encontró la tarea."
        )
        return

    print()
    print(
        "Deje un campo vacío para "
        "conservar su valor actual."
    )

    titulo = input(
        f"Título [{tarea.titulo}]: "
    ).strip()

    if not titulo:
        titulo = tarea.titulo

    descripcion = input(
        f"Descripción "
        f"[{tarea.descripcion}]: "
    ).strip()

    if not descripcion:
        descripcion = tarea.descripcion

    categoria = input(
        f"Categoría "
        f"[{tarea.categoria}]: "
    ).strip()

    if not categoria:
        categoria = tarea.categoria

    prioridad = seleccionar_prioridad(
        tarea.prioridad
    )

    estado = seleccionar_estado(
        tarea.estado
    )

    fecha_actual = (
        tarea.fecha_limite
        if tarea.fecha_limite
        else "Sin fecha"
    )

    fecha_limite = input(
        f"Fecha límite [{fecha_actual}]: "
    ).strip()

    if not fecha_limite:
        fecha_limite = tarea.fecha_limite

    try:
        actualizada = (
            servicio_tareas.actualizar_tarea(
                id_tarea=id_tarea,
                titulo=titulo,
                descripcion=descripcion,
                prioridad=prioridad,
                estado=estado,
                categoria=categoria,
                fecha_limite=fecha_limite,
            )
        )

        if actualizada:
            print(
                "Tarea actualizada "
                "correctamente."
            )

        else:
            print(
                "No se pudo actualizar "
                "la tarea."
            )

    except ValueError as error:
        print(
            f"Error: {error}"
        )


def cambiar_estado_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "\nID de la tarea "
                "que desea modificar: "
            )
        )

    except ValueError:
        print(
            "El ID introducido "
            "no es válido."
        )
        return

    tarea = servicio_tareas.obtener_tarea(
        id_tarea
    )

    if tarea is None:
        print(
            "No se encontró la tarea."
        )
        return

    nuevo_estado = seleccionar_estado(
        tarea.estado
    )

    try:
        actualizado = (
            servicio_tareas.cambiar_estado(
                id_tarea,
                nuevo_estado,
            )
        )

        if actualizado:
            print(
                f'Estado actualizado a '
                f'"{nuevo_estado}".'
            )

        else:
            print(
                "No se pudo actualizar "
                "el estado."
            )

    except ValueError as error:
        print(
            f"Error: {error}"
        )


def eliminar_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "\nID de la tarea "
                "que desea eliminar: "
            )
        )

    except ValueError:
        print(
            "El ID introducido "
            "no es válido."
        )
        return

    tarea = servicio_tareas.obtener_tarea(
        id_tarea
    )

    if tarea is None:
        print(
            "No se encontró la tarea."
        )
        return

    confirmacion = input(
        f'¿Desea eliminar '
        f'"{tarea.titulo}"? (s/n): '
    ).strip().lower()

    if confirmacion != "s":
        print(
            "Eliminación cancelada."
        )
        return

    if servicio_tareas.eliminar_tarea(
        id_tarea
    ):
        print(
            "Tarea eliminada "
            "correctamente."
        )

    else:
        print(
            "No se pudo eliminar "
            "la tarea."
        )


def buscar_tareas() -> None:
    print()
    print("--- Buscar tareas ---")

    texto = input(
        "Texto a buscar: "
    ).strip()

    tareas = servicio_tareas.buscar_tareas(
        texto
    )

    mostrar_lista(
        tareas,
        f'Resultados para "{texto}"',
    )


def filtrar_tareas() -> None:
    print()
    print("--- Filtrar tareas ---")
    print("1. Por estado")
    print("2. Por prioridad")
    print("3. Volver")

    opcion = input(
        "\nSeleccione un filtro: "
    ).strip()

    if opcion == "1":

        estado = seleccionar_estado()

        tareas = (
            servicio_tareas.filtrar_por_estado(
                estado
            )
        )

        mostrar_lista(
            tareas,
            f"Estado: {estado}",
        )

    elif opcion == "2":

        prioridad = seleccionar_prioridad()

        tareas = (
            servicio_tareas.filtrar_por_prioridad(
                prioridad
            )
        )

        mostrar_lista(
            tareas,
            f"Prioridad: {prioridad}",
        )

    elif opcion == "3":
        return

    else:
        print(
            "Filtro no válido."
        )


def mostrar_tareas_vencidas() -> None:
    tareas = (
        servicio_tareas.obtener_tareas_vencidas()
    )

    mostrar_lista(
        tareas,
        "Tareas vencidas",
    )


def mostrar_por_fecha() -> None:
    tareas = (
        servicio_tareas.obtener_tareas_por_fecha()
    )

    mostrar_lista(
        tareas,
        "Tareas ordenadas por fecha límite",
    )


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
                buscar_tareas()

            case "7":
                filtrar_tareas()

            case "8":
                mostrar_tareas_vencidas()

            case "9":
                mostrar_por_fecha()

            case "0":
                print()
                print(
                    "Gracias por utilizar "
                    "el Gestor de Tareas."
                )
                break

            case _:
                print()
                print(
                    "La opción seleccionada "
                    "no es válida."
                )


if __name__ == "__main__":
    main()