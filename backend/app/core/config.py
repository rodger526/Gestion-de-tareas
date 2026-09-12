from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    nombre_app: str = "Gestor de Tareas"
    version: str = "1.0.0"

    database_url: str

    secret_key: str

    algoritmo: str = "HS256"

    minutos_token: int = 1440

    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def obtener_configuracion() -> Configuracion:
    return Configuracion()


configuracion = obtener_configuracion()