import os
from sqlalchemy import create_engine         #type: ignore
from sqlalchemy.ext.declarative import declarative_base     #type: ignore
from sqlalchemy.orm import sessionmaker, Session     #type: ignore

# Base para todos los modelos ORM
Base = declarative_base()

# URL de base de datos (configurable por .env)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Crear engine
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False") == "True",
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Dependency para obtener sesión de BD."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa la base de datos creando todas las tablas."""
    Base.metadata.create_all(bind=engine)
