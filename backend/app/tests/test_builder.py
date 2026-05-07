import pytest
from datetime import datetime

from app.domain.factories.audit_log_builder import AuditLogBuilder


def test_builder_completo():
    """Test: builder con todos los campos retorna objeto válido."""
    timestamp = datetime.utcnow()
    
    audit_log = (
        AuditLogBuilder()
        .set_actor(1)
        .set_entity("REQUEST", 42)
        .set_action("APPROVED")
        .set_state_transition("SUBMITTED", "APPROVED")
        .set_description("Aprobado por gerente")
        .set_timestamp(timestamp)
        .build()
    )
    
    assert audit_log.actor_id == 1
    assert audit_log.entity_type == "REQUEST"
    assert audit_log.entity_id == 42
    assert audit_log.action == "APPROVED"
    assert audit_log.previous_state == "SUBMITTED"
    assert audit_log.new_state == "APPROVED"
    assert audit_log.description == "Aprobado por gerente"
    assert audit_log.timestamp == timestamp


def test_builder_campos_obligatorios():
    """Test: builder sin campo obligatorio lanza excepción."""
    with pytest.raises(ValueError, match="actor_id es requerido"):
        AuditLogBuilder().build()


def test_builder_sin_entity():
    """Test: builder sin entity lanza excepción."""
    with pytest.raises(ValueError, match="entity_type es requerido"):
        AuditLogBuilder().set_actor(1).build()


def test_builder_sin_action():
    """Test: builder sin action lanza excepción."""
    with pytest.raises(ValueError, match="action es requerida"):
        (
            AuditLogBuilder()
            .set_actor(1)
            .set_entity("REQUEST", 42)
            .build()
        )


def test_builder_fluent_api():
    """Test: fluent API retorna el builder."""
    builder = AuditLogBuilder()
    result = builder.set_actor(1)
    assert result is builder


def test_builder_con_opcionales():
    """Test: builder con campos opcionales."""
    audit_log = (
        AuditLogBuilder()
        .set_actor(1)
        .set_entity("USER", 100)
        .set_action("CREATED")
        .build()
    )
    
    assert audit_log.previous_state is None
    assert audit_log.new_state is None
    assert audit_log.description is None

