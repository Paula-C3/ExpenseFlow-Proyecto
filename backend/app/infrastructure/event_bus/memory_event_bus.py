from typing import Dict, List, Type

from app.domain.interfaces.event_bus import IEventBus, DomainEvent, IEventListener


class MemoryEventBus(IEventBus):
    """Implementación en memoria del Event Bus."""

    def __init__(self):
        self._subscribers: Dict[Type[DomainEvent], List[IEventListener]] = {}

    def publish(self, event: DomainEvent) -> None:
        """Publica un evento a todos los suscriptores."""
        event_type = type(event)
        if event_type in self._subscribers:
            for listener in self._subscribers[event_type]:
                listener.handle(event)

    def subscribe(self, event_type: Type[DomainEvent], listener: IEventListener) -> None:
        """Se suscribe a un tipo de evento."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(listener)

    def get_subscribers(self, event_type: Type[DomainEvent]) -> List[IEventListener]:
        """Obtiene los suscriptores de un tipo de evento."""
        return self._subscribers.get(event_type, [])
