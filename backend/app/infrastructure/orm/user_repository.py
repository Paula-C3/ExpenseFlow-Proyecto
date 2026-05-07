from typing import Optional, List
from sqlalchemy.orm import Session

from backend.app.domain.entities.user import User
from backend.app.domain.interfaces.user_repository import IUserRepository
from backend.app.infrastructure.orm.user_model import UserModel


class SQLUserRepository(IUserRepository):
    """Implementación de IUserRepository con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        """Guarda un nuevo usuario."""
        db_user = UserModel.from_domain(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user.id = db_user.id
        self.db.refresh(db_user)
        return db_user.to_domain()

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuario por ID."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return db_user.to_domain() if db_user else None

    def find_by_email(self, email: str) -> Optional[User]:
        """Busca usuario por email."""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return db_user.to_domain() if db_user else None

    def find_all(self) -> List[User]:
        """Retorna todos los usuarios."""
        db_users = self.db.query(UserModel).all()
        return [user.to_domain() for user in db_users]

    def update(self, user: User) -> User:
        """Actualiza un usuario."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            raise ValueError(f"Usuario {user.id} no encontrado")
        
        db_user.email = str(user.email) if user.email else db_user.email
        db_user.full_name = user.full_name
        db_user.hashed_password = user.hashed_password
        db_user.is_active = user.is_active
        db_user.role_id = user.role_id
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user.to_domain()

    def delete(self, user_id: int) -> None:
        """Elimina un usuario."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
