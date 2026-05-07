import pytest                   #type: ignore
from unittest.mock import MagicMock
from fastapi.testclient import TestClient #type: ignore

from backend.app.main import app
from backend.app.api.dependencies import get_current_user
from backend.app.infrastructure.database import get_db
from app.domain.factories.singleton import EventBusRegistry
from app.infrastructure.event_bus.memory_event_bus import MemoryEventBus


def make_user(user_id: int, role: str, email: str = "test@test.com") -> dict:
    return {"sub": str(user_id), "role": role, "email": email}



@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def employee_client(mock_db):
    user = make_user(user_id=1, role="EMPLOYEE")
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def admin_client(mock_db):
    user = make_user(user_id=99, role="SYSTEM_ADMIN")
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: user
    yield TestClient(app)
    app.dependency_overrides.clear()
    
@pytest.fixture(autouse=True)
def setup_event_bus():
    EventBusRegistry().set_event_bus(MemoryEventBus())