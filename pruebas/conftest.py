import pytest

from app.base_datos.conexion import inicializar_base_datos
from app.servicios.servicio_tareas import ServicioTareas


@pytest.fixture
def servicio(tmp_path):
    ruta_base_datos = (
        tmp_path / "gestor_tareas_pruebas.db"
    )

    inicializar_base_datos(
        ruta_base_datos
    )

    return ServicioTareas(
        ruta_base_datos=ruta_base_datos
    )