import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database import Base
from app.infrastructure.orm.request_model import RequestModel
from app.infrastructure.orm.user_model import UserModel
from app.infrastructure.orm.request_repository import SQLRequestRepository
from app.infrastructure.orm.user_repository import SQLUserRepository
from app.domain.entities.request import Request
from app.domain.entities.user import User
from app.domain.value_objects import Email

# Configuración de base de datos en memoria para pruebas
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()

def test_save_and_find_request(db_session):
    repo = SQLRequestRepository(db_session)
    request = Request(
        id=None,
        employee_id=1,
        title="Compra laptop",
        description="Equipo nuevo",
        amount=None,
        category="IT",
        receipt_url="http://comprobante.com",
        status="SUBMITTED",
        submitted_by_id=1,
        manager_id=None,
        finance_id=None,
    )
    saved = repo.save(request)
    found = repo.find_by_id(saved.id)
    assert found is not None
    assert found.title == "Compra laptop"

def test_update_request(db_session):
    repo = SQLRequestRepository(db_session)
    request = Request(
        id=None,
        employee_id=1,
        title="Compra mouse",
        description="Accesorio",
        amount=None,
        category="IT",
        receipt_url="http://comprobante.com",
        status="SUBMITTED",
        submitted_by_id=1,
        manager_id=None,
        finance_id=None,
    )
    saved = repo.save(request)
    saved.title = "Compra teclado"
    updated = repo.update(saved)
    assert updated.title == "Compra teclado"

def test_delete_request(db_session):
    repo = SQLRequestRepository(db_session)
    request = Request(
        id=None,
        employee_id=1,
        title="Compra monitor",
        description="Pantalla",
        amount=None,
        category="IT",
        receipt_url="http://comprobante.com",
        status="SUBMITTED",
        submitted_by_id=1,
        manager_id=None,
        finance_id=None,
    )
    saved = repo.save(request)
    repo.delete(saved.id)
    assert repo.find_by_id(saved.id) is None

def test_save_and_find_user(db_session):
    repo = SQLUserRepository(db_session)
    user = User(
        id=None,
        email=Email("test@example.com"),
        full_name="Ayelén",
        hashed_password="hashed123",
        is_active=True,
        role_id=1,
    )
    saved = repo.save(user)
    found = repo.find_by_email("test@example.com")
    assert found is not None
    assert found.full_name == "Ayelén"

def test_update_user(db_session):
    repo = SQLUserRepository(db_session)
    user = User(
        id=None,
        email=Email("update@example.com"),
        full_name="Paula",
        hashed_password="hashed123",
        is_active=True,
        role_id=1,
    )
    saved = repo.save(user)
    saved.full_name = "Paula Actualizada"
    updated = repo.update(saved)
    assert updated.full_name == "Paula Actualizada"

def test_delete_user(db_session):
    repo = SQLUserRepository(db_session)
    user = User(
        id=None,
        email=Email("delete@example.com"),
        full_name="Giuliana",
        hashed_password="hashed123",
        is_active=True,
        role_id=1,
    )
    saved = repo.save(user)
    repo.delete(saved.id)
    assert repo.find_by_id(saved.id) is None
