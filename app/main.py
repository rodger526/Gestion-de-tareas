from app.base_datos.conexion import inicializar_base_datos
from app.servicios.servicio_tareas import ServicioTareas


servicio_tareas = ServicioTareas()


def mostrar_encabezado() -> None:
    print()
    print("=" * 50)
    print("              GESTOR DE TAREAS")
    print("=" * 50)


def mostrar_menu() -> None:
    print()
    print("1. Crear tarea")
    print("2. Ver tareas")
    print("3. Editar tarea")
    print("4. Completar / reabrir tarea")
    print("5. Eliminar tarea")
    print("6. Salir")
    print()


def crear_tarea() -> None:
    print("\n--- Crear tarea ---")

    titulo = input("Título: ")
    descripcion = input("Descripción: ")

    try:
        tarea = servicio_tareas.crear_tarea(
            titulo=titulo,
            descripcion=descripcion,
        )

        print(
            f"\nTarea #{tarea.id} creada correctamente."
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

        estado = "✓" if tarea.completada else "○"

        print(
            f"{estado} [{tarea.id}] "
            f"{tarea.titulo}"
        )

        if tarea.descripcion:
            print(
                f"    Descripción: "
                f"{tarea.descripcion}"
            )


def editar_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input("\nID de la tarea que desea editar: ")
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

    try:
        actualizada = servicio_tareas.actualizar_tarea(
            id_tarea=id_tarea,
            titulo=titulo,
            descripcion=descripcion,
        )

        if actualizada:
            print("Tarea actualizada correctamente.")
        else:
            print("No se pudo actualizar la tarea.")

    except ValueError as error:
        print(f"Error: {error}")


def cambiar_estado_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "\nID de la tarea que desea "
                "completar o reabrir: "
            )
        )

    except ValueError:
        print("El ID introducido no es válido.")
        return

    tarea = servicio_tareas.obtener_tarea(id_tarea)

    if tarea is None:
        print("No se encontró la tarea.")
        return

    if servicio_tareas.cambiar_estado(id_tarea):

        if tarea.completada:
            print("La tarea ha sido reabierta.")
        else:
            print("La tarea ha sido completada.")

    else:
        print(
            "No se pudo cambiar el estado "
            "de la tarea."
        )


def eliminar_tarea() -> None:
    mostrar_tareas()

    try:
        id_tarea = int(
            input(
                "\nID de la tarea que desea eliminar: "
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
        f'¿Desea eliminar "{tarea.titulo}"? (s/n): '
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