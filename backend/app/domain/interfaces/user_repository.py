from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.user import User


class IUserRepository(ABC):
    """Interfaz para repositorio de usuarios."""

    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda un usuario."""
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuario por ID."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca usuario por email."""
        pass

    @abstractmethod
    def find_all(self) -> List[User]:
        """Retorna todos los usuarios."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        """Elimina un usuario."""
        pass

