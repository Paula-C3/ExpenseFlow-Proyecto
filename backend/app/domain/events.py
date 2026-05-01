from dataclasses import dataclass
from datetime import datetime

from backend.app.domain.interfaces.event_bus import DomainEvent
from backend.app.domain.enums import RequestStatus


@dataclass
class RequestCreatedEvent(DomainEvent):
    """Evento: Solicitud creada."""
    request_id: int
    employee_id: int
    title: str
    amount: float
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class RequestSubmittedEvent(DomainEvent):
    """Evento: Solicitud enviada."""
    request_id: int
    submitted_by_id: int
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class RequestApprovedEvent(DomainEvent):
    """Evento: Solicitud aprobada."""
    request_id: int
    approver_id: int
    comment: str = ""
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class RequestRejectedEvent(DomainEvent):
    """Evento: Solicitud rechazada."""
    request_id: int
    rejector_id: int
    reason: str = ""
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class RequestStatusChangedEvent(DomainEvent):
    """Evento: Estado de solicitud cambió."""
    request_id: int
    previous_status: RequestStatus
    new_status: RequestStatus
    actor_id: int
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class NotificationCreatedEvent(DomainEvent):
    """Evento: Notificación creada."""
    notification_id: int
    user_id: int
    message: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

