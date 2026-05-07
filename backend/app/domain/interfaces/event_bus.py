from abc import ABC, abstractmethod
from typing import List


class DomainEvent(ABC):
    """Clase base para eventos del dominio."""
    pass


class IEventListener(ABC):
    """Interfaz para listeners de eventos."""

    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        """Maneja un evento del dominio."""
        pass


class IEventBus(ABC):
    """Interfaz para el bus de eventos."""

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """Publica un evento."""
        pass

    @abstractmethod
    def subscribe(self, event_type: type, listener: IEventListener) -> None:
        """Se suscribe a un tipo de evento."""
        pass

    @abstractmethod
    def get_subscribers(self, event_type: type) -> List[IEventListener]:
        """Obtiene los suscriptores de un tipo de evento."""
        pass
