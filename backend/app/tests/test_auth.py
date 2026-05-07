import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.infrastructure.database import Base, get_db

# Configuración de DB para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_register_and_login():
    # Registro
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "full_name": "Ayelén",
        "password": "secret123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    # Login correcto
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    login_data = response.json()
    assert "access_token" in login_data

    # Login incorrecto
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_me_endpoint():
    # Registro para obtener token
    response = client.post("/auth/register", json={
        "email": "me@example.com",
        "full_name": "Paula",
        "password": "secret123"
    })
    token = response.json()["access_token"]

    # Usar token en /auth/me
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_info = response.json()
    assert user_info["email"] == "me@example.com"

def test_users_requires_admin():
    # Registro normal (EMPLOYEE)
    response = client.post("/auth/register", json={
        "email": "employee@example.com",
        "full_name": "Giuliana",
        "password": "secret123"
    })
    token = response.json()["access_token"]

    # Intentar acceder a /auth/users sin ser admin
    response = client.get("/auth/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
