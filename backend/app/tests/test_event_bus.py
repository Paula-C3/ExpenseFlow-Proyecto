import pytest
from datetime import datetime

from app.domain.entities.request import Request
from app.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from app.domain.events import RequestApprovedEvent, RequestRejectedEvent
from app.domain.interfaces.event_bus import IEventListener, DomainEvent


class MockAuditListener(IEventListener):
    """Mock listener para audit logs."""
    
    def __init__(self):
        self.events = []
    
    def handle(self, event: DomainEvent) -> None:
        self.events.append(event)
        print(f"📜 AuditLog: Request {event.request_id} - Action: {type(event).__name__}")


class MockNotificationListener(IEventListener):
    """Mock listener para notificaciones."""
    
    def __init__(self):
        self.events = []
    
    def handle(self, event: DomainEvent) -> None:
        self.events.append(event)
        print(f"🔔 Notification: Request {event.request_id} - User: {getattr(event, 'approver_id', 'N/A')}")


def test_event_bus_with_request_approval():
    """Test: Request approval dispara eventos automáticamente."""
    
    # Arrange
    bus = MemoryEventBus()
    audit_listener = MockAuditListener()
    notification_listener = MockNotificationListener()
    
    bus.subscribe(RequestApprovedEvent, audit_listener)
    bus.subscribe(RequestApprovedEvent, notification_listener)
    
    request = Request(
        id=1,
        title="Compra laptop",
        user_id=10,
        approver_id=5,
        event_bus=bus
    )
    
    # Act
    request.approve()
    
    # Assert
    assert len(audit_listener.events) == 1
    assert len(notification_listener.events) == 1
    
    event = audit_listener.events[0]
    assert isinstance(event, RequestApprovedEvent)
    assert event.request_id == 1
    assert event.approver_id == 5


def test_event_bus_with_request_rejection():
    """Test: Request rejection dispara eventos automáticamente."""
    
    # Arrange
    bus = MemoryEventBus()
    audit_listener = MockAuditListener()
    notification_listener = MockNotificationListener()
    
    bus.subscribe(RequestRejectedEvent, audit_listener)
    bus.subscribe(RequestRejectedEvent, notification_listener)
    
    request = Request(
        id=2,
        title="Compra mouse",
        user_id=10,
        approver_id=5,
        event_bus=bus
    )
    
    # Act
    request.reject()
    
    # Assert
    assert len(audit_listener.events) == 1
    assert len(notification_listener.events) == 1
    
    event = audit_listener.events[0]
    assert isinstance(event, RequestRejectedEvent)
    assert event.request_id == 2
    assert event.rejector_id == 5


def test_event_bus_without_bus():
    """Test: Request sin event_bus no dispara eventos."""
    
    # Arrange
    request = Request(
        id=3,
        title="Compra teclado",
        user_id=10,
        event_bus=None
    )
    
    # Act - Should not raise
    request.approve()
    
    # Assert - No events published
    assert True  # Simplemente verificar que no hay excepción


def test_multiple_subscribers_same_event():
    """Test: Múltiples subscribers escuchan el mismo evento."""
    
    # Arrange
    bus = MemoryEventBus()
    listeners = [MockAuditListener() for _ in range(3)]
    
    for listener in listeners:
        bus.subscribe(RequestApprovedEvent, listener)
    
    request = Request(
        id=4,
        title="Compra monitor",
        user_id=10,
        approver_id=5,
        event_bus=bus
    )
    
    # Act
    request.approve()
    
    # Assert
    for listener in listeners:
        assert len(listener.events) == 1
        assert listener.events[0].request_id == 4


def test_event_has_timestamp():
    """Test: Los eventos incluyen timestamp."""
    
    # Arrange
    bus = MemoryEventBus()
    listener = MockAuditListener()
    bus.subscribe(RequestApprovedEvent, listener)
    
    request = Request(
        id=5,
        title="Compra silla",
        user_id=10,
        approver_id=5,
        event_bus=bus
    )
    
    before_time = datetime.utcnow()
    
    # Act
    request.approve()
    
    after_time = datetime.utcnow()
    
    # Assert
    event = listener.events[0]
    assert hasattr(event, 'timestamp')
    assert before_time <= event.timestamp <= after_time


if __name__ == "__main__":
    # Ejecutar tests con pytest
    pytest.main([__file__, "-v", "-s"])
