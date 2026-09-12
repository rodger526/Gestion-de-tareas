from fastapi.testclient import TestClient

from app.api import app


cliente = TestClient(app)


def test_inicio():
    respuesta = cliente.get(
        "/"
    )

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert datos["nombre"] == (
        "Gestor de Tareas API"
    )


def test_health():
    respuesta = cliente.get(
        "/health"
    )

    assert respuesta.status_code == 200

    assert respuesta.json() == {
        "status": "ok"
    }


def test_listar_tareas():
    respuesta = cliente.get(
        "/tareas"
    )

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert "total" in datos
    assert "pagina" in datos
    assert "limite" in datos
    assert "tareas" in datos


def test_paginacion():
    respuesta = cliente.get(
        "/tareas?pagina=1&limite=5"
    )

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert datos["pagina"] == 1
    assert datos["limite"] == 5


def test_limite_invalido():
    respuesta = cliente.get(
        "/tareas?limite=500"
    )

    assert respuesta.status_code == 422


def test_pagina_invalida():
    respuesta = cliente.get(
        "/tareas?pagina=0"
    )

    assert respuesta.status_code == 422


def test_obtener_tarea_inexistente():
    respuesta = cliente.get(
        "/tareas/999999"
    )

    assert respuesta.status_code == 404

    assert respuesta.json() == {
        "detail": "Tarea no encontrada."
    }