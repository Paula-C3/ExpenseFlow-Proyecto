from app.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from app.domain.events import RequestSubmittedEvent, RequestApprovedEvent
from app.domain.interfaces.event_bus import IEventListener, DomainEvent


class MockListener(IEventListener):
    def __init__(self):
        self.received = []
    def handle(self, event: DomainEvent):
        self.received.append(event)


def test_listener_called_on_submitted():
    bus = MemoryEventBus()
    listener = MockListener()
    bus.subscribe(RequestSubmittedEvent, listener)

    bus.publish(RequestSubmittedEvent(request_id=1, submitted_by_id=2))

    assert len(listener.received) == 1
    assert listener.received[0].request_id == 1


def test_listener_not_called_for_different_event():
    bus = MemoryEventBus()
    listener = MockListener()
    bus.subscribe(RequestSubmittedEvent, listener)

    bus.publish(RequestApprovedEvent(request_id=1, approver_id=5))

    assert len(listener.received) == 0


def test_multiple_listeners_same_event():
    bus = MemoryEventBus()
    l1, l2 = MockListener(), MockListener()
    bus.subscribe(RequestApprovedEvent, l1)
    bus.subscribe(RequestApprovedEvent, l2)

    bus.publish(RequestApprovedEvent(request_id=10, approver_id=3))

    assert len(l1.received) == 1
    assert len(l2.received) == 1
