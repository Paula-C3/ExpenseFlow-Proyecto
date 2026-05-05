import pytest

from app.domain.factories.singleton import Settings, EventBusRegistry


def test_settings_singleton():
    """Test: dos llamadas a Settings retornan el mismo objeto."""
    settings1 = Settings()
    settings2 = Settings()
    
    assert settings1 is settings2
    assert id(settings1) == id(settings2)


def test_settings_persists_data():
    """Test: datos persisten entre instancias."""
    settings1 = Settings()
    settings1.set_database_url("postgresql://localhost:5432/db")
    settings1.set_secret_key("secret123")
    
    settings2 = Settings()
    assert settings2.database_url == "postgresql://localhost:5432/db"
    assert settings2.secret_key == "secret123"


def test_event_bus_registry_singleton():
    """Test: dos llamadas a EventBusRegistry retornan el mismo objeto."""
    registry1 = EventBusRegistry()
    registry2 = EventBusRegistry()
    
    assert registry1 is registry2
    assert id(registry1) == id(registry2)


def test_event_bus_registry_persists_event_bus():
    """Test: event bus persiste entre instancias."""
    from app.infrastructure.event_bus.memory_event_bus import MemoryEventBus
    
    registry1 = EventBusRegistry()
    event_bus = MemoryEventBus()
    registry1.set_event_bus(event_bus)
    
    registry2 = EventBusRegistry()
    assert registry2.get_event_bus() is event_bus


def test_event_bus_registry_not_set():
    """Test: obtener event bus sin establecer lanza error."""
    # Limpiar registry
    EventBusRegistry._instances.clear()
    
    registry = EventBusRegistry()
    with pytest.raises(RuntimeError, match="Event bus no ha sido registrado"):
        registry.get_event_bus()
