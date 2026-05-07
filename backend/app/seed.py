"""
Script para poblar la base de datos con usuarios de prueba.
Ejecutar desde la raíz del proyecto:
    docker compose exec backend python backend/app/seed.py
"""

import sys

sys.path.insert(0, "/app")

from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal, init_db
from app.infrastructure.orm.user_model import UserModel, RoleModel
from app.infrastructure.security import hash_password
from app.domain.enums import RoleType


ROLES = [
    RoleType.EMPLOYEE,
    RoleType.MANAGER,
    RoleType.FINANCE_ANALYST,
    RoleType.FINANCE_ADMIN,
    RoleType.SYSTEM_ADMIN,
]

TEST_USERS = [
    {
        "email": "admin@test.com",
        "full_name": "Admin User",
        "password": "admin123",
        "role": RoleType.SYSTEM_ADMIN,
    },
    {
        "email": "manager@test.com",
        "full_name": "Manager User",
        "password": "manager123",
        "role": RoleType.MANAGER,
    },
    {
        "email": "employee@test.com",
        "full_name": "Employee User",
        "password": "emp123",
        "role": RoleType.EMPLOYEE,
    },
    {
        "email": "analyst@test.com",
        "full_name": "Finance Analyst",
        "password": "analyst123",
        "role": RoleType.FINANCE_ANALYST,
    },
    {
        "email": "finance@test.com",
        "full_name": "Finance Admin",
        "password": "finance123",
        "role": RoleType.FINANCE_ADMIN,
    },
]


def seed():
    init_db()
    db: Session = SessionLocal()

    try:
        # crear roles si no existen
        role_map = {}
        for role_type in ROLES:
            existing = db.query(RoleModel).filter(RoleModel.name == role_type).first()
            if not existing:
                role = RoleModel(name=role_type, description=role_type.value)
                db.add(role)
                db.commit()
                db.refresh(role)
                role_map[role_type] = role
                print(f"Rol creado: {role_type.value}")
            else:
                role_map[role_type] = existing
                print(f"Rol ya existe: {role_type.value}")

        # crear usuarios si no existen
        for user_data in TEST_USERS:
            existing = db.query(UserModel).filter(
                UserModel.email == user_data["email"]
            ).first()
            if not existing:
                user = UserModel(
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    hashed_password=hash_password(user_data["password"]),
                    role_id=role_map[user_data["role"]].id,
                    is_active=True,
                )
                db.add(user)
                db.commit()
                print(f"Usuario creado: {user_data['email']} ({user_data['role'].value})")
            else:
                print(f"Usuario ya existe: {user_data['email']}")

        print("\nSeed completado.")

    except Exception as e:
        db.rollback()
        print(f"Error durante el seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()