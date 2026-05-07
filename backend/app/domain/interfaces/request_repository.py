from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.request import Request
from app.domain.enums import RequestStatus, RoleType


class IRequestRepository(ABC):
    """Interfaz para repositorio de solicitudes."""

    @abstractmethod
    def save(self, request: Request) -> Request:
        """Guarda una solicitud."""
        pass

    @abstractmethod
    def find_by_id(self, request_id: int) -> Optional[Request]:
        """Busca solicitud por ID."""
        pass

    @abstractmethod
    def find_by_status(self, status: RequestStatus) -> List[Request]:
        """Encuentra solicitudes por estado."""
        pass

    @abstractmethod
    def find_by_employee(self, employee_id: int) -> List[Request]:
        """Encuentra solicitudes de un empleado."""
        pass

    @abstractmethod
    def find_by_role(self, role: RoleType) -> List[Request]:
        """Encuentra solicitudes según el rol."""
        pass

    @abstractmethod
    def find_all(self) -> List[Request]:
        """Retorna todas las solicitudes."""
        pass

    @abstractmethod
    def update(self, request: Request) -> Request:
        """Actualiza una solicitud."""
        pass

    @abstractmethod
    def delete(self, request_id: int) -> None:
        """Elimina una solicitud."""
        pass

