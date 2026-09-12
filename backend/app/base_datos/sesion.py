from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import configuracion


motor = create_engine(
    configuracion.database_url,
    pool_pre_ping=True,
)

SesionLocal = sessionmaker(
    bind=motor,
    autoflush=False,
    autocommit=False,
)


def obtener_db():
    db = SesionLocal()

    try:
        yield db
    finally:
        db.close()