import pytest


def test_crear_tarea(servicio):
    tarea = servicio.crear_tarea(
        titulo="Aprender FastAPI",
        descripcion="Estudiar endpoints",
        prioridad="Alta",
        categoria="Programación",
        fecha_limite="2026-12-20",
    )

    assert tarea.id is not None
    assert tarea.titulo == "Aprender FastAPI"
    assert tarea.descripcion == "Estudiar endpoints"
    assert tarea.prioridad == "Alta"
    assert tarea.estado == "Pendiente"
    assert tarea.categoria == "Programación"
    assert tarea.fecha_limite == "2026-12-20"


def test_crear_tarea_con_titulo_vacio(servicio):
    with pytest.raises(ValueError):
        servicio.crear_tarea(
            titulo=""
        )


def test_prioridad_invalida(servicio):
    with pytest.raises(ValueError):
        servicio.crear_tarea(
            titulo="Tarea",
            prioridad="Super importante",
        )


def test_estado_invalido(servicio):
    with pytest.raises(ValueError):
        servicio.crear_tarea(
            titulo="Tarea",
            estado="Cancelada",
        )


def test_fecha_invalida(servicio):
    with pytest.raises(ValueError):
        servicio.crear_tarea(
            titulo="Tarea",
            fecha_limite="20/12/2026",
        )


def test_obtener_tarea(servicio):
    creada = servicio.crear_tarea(
        titulo="Aprender SQLite"
    )

    obtenida = servicio.obtener_tarea(
        creada.id
    )

    assert obtenida is not None
    assert obtenida.id == creada.id
    assert obtenida.titulo == "Aprender SQLite"


def test_obtener_tarea_inexistente(servicio):
    tarea = servicio.obtener_tarea(
        9999
    )

    assert tarea is None


def test_actualizar_tarea(servicio):
    tarea = servicio.crear_tarea(
        titulo="Título original"
    )

    resultado = servicio.actualizar_tarea(
        id_tarea=tarea.id,
        titulo="Título modificado",
        descripcion="Nueva descripción",
        prioridad="Urgente",
        estado="En progreso",
        categoria="Universidad",
        fecha_limite="2026-12-25",
    )

    actualizada = servicio.obtener_tarea(
        tarea.id
    )

    assert resultado is True
    assert actualizada is not None
    assert actualizada.titulo == "Título modificado"
    assert actualizada.descripcion == "Nueva descripción"
    assert actualizada.prioridad == "Urgente"
    assert actualizada.estado == "En progreso"
    assert actualizada.categoria == "Universidad"
    assert actualizada.fecha_limite == "2026-12-25"


def test_cambiar_estado(servicio):
    tarea = servicio.crear_tarea(
        titulo="Terminar proyecto"
    )

    resultado = servicio.cambiar_estado(
        tarea.id,
        "Completada",
    )

    actualizada = servicio.obtener_tarea(
        tarea.id
    )

    assert resultado is True
    assert actualizada is not None
    assert actualizada.estado == "Completada"


def test_eliminar_tarea(servicio):
    tarea = servicio.crear_tarea(
        titulo="Eliminar esta tarea"
    )

    resultado = servicio.eliminar_tarea(
        tarea.id
    )

    assert resultado is True

    tarea_eliminada = servicio.obtener_tarea(
        tarea.id
    )

    assert tarea_eliminada is None


def test_buscar_por_titulo(servicio):
    servicio.crear_tarea(
        titulo="Aprender Python"
    )

    servicio.crear_tarea(
        titulo="Estudiar bases de datos"
    )

    resultados = servicio.buscar_tareas(
        "Python"
    )

    assert len(resultados) == 1
    assert resultados[0].titulo == "Aprender Python"


def test_buscar_por_categoria(servicio):
    servicio.crear_tarea(
        titulo="Proyecto final",
        categoria="Universidad",
    )

    servicio.crear_tarea(
        titulo="Comprar comida",
        categoria="Personal",
    )

    resultados = servicio.buscar_tareas(
        "Universidad"
    )

    assert len(resultados) == 1
    assert resultados[0].categoria == "Universidad"


def test_filtrar_por_prioridad(servicio):
    servicio.crear_tarea(
        titulo="Tarea urgente",
        prioridad="Urgente",
    )

    servicio.crear_tarea(
        titulo="Tarea normal",
        prioridad="Media",
    )

    resultados = (
        servicio.filtrar_por_prioridad(
            "Urgente"
        )
    )

    assert len(resultados) == 1
    assert resultados[0].prioridad == "Urgente"


def test_filtrar_por_estado(servicio):
    tarea = servicio.crear_tarea(
        titulo="Tarea activa"
    )

    servicio.cambiar_estado(
        tarea.id,
        "En progreso",
    )

    servicio.crear_tarea(
        titulo="Tarea pendiente"
    )

    resultados = (
        servicio.filtrar_por_estado(
            "En progreso"
        )
    )

    assert len(resultados) == 1
    assert resultados[0].estado == "En progreso"


def test_tarea_vencida(servicio):
    servicio.crear_tarea(
        titulo="Tarea vencida",
        fecha_limite="2020-01-01",
    )

    servicio.crear_tarea(
        titulo="Tarea futura",
        fecha_limite="2099-01-01",
    )

    resultados = (
        servicio.obtener_tareas_vencidas()
    )

    titulos = [
        tarea.titulo
        for tarea in resultados
    ]

    assert "Tarea vencida" in titulos
    assert "Tarea futura" not in titulos


def test_tarea_completada_no_aparece_como_vencida(
    servicio,
):
    tarea = servicio.crear_tarea(
        titulo="Tarea antigua",
        fecha_limite="2020-01-01",
    )

    servicio.cambiar_estado(
        tarea.id,
        "Completada",
    )

    resultados = (
        servicio.obtener_tareas_vencidas()
    )

    ids = [
        tarea.id
        for tarea in resultados
    ]

    assert tarea.id not in ids


def test_ordenar_por_fecha(servicio):
    servicio.crear_tarea(
        titulo="Última",
        fecha_limite="2026-12-30",
    )

    servicio.crear_tarea(
        titulo="Primera",
        fecha_limite="2026-10-01",
    )

    servicio.crear_tarea(
        titulo="Sin fecha",
    )

    resultados = (
        servicio.obtener_tareas_por_fecha()
    )

    assert resultados[0].titulo == "Primera"
    assert resultados[1].titulo == "Última"
    assert resultados[2].titulo == "Sin fecha"