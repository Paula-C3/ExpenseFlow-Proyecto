import pytest
from app.domain.factories.audit_log_builder import AuditLogBuilder


def test_audit_log_built_correctly():
    log = (
        AuditLogBuilder()
        .set_actor(5)
        .set_entity("REQUEST", 1)
        .set_action("APPROVED")
        .set_state_transition("SUBMITTED", "APPROVED")
        .build()
    )
    assert log.actor_id == 5
    assert log.entity_id == 1
    assert log.previous_state == "SUBMITTED"
    assert log.new_state == "APPROVED"
    assert log.action == "APPROVED"


def test_audit_log_missing_actor_raises():
    with pytest.raises(ValueError, match="actor_id"):
        AuditLogBuilder().set_entity("REQUEST", 1).set_action("X").build()


def test_audit_log_missing_entity_raises():
    with pytest.raises(ValueError, match="entity_type"):
        AuditLogBuilder().set_actor(1).set_action("X").build()


def test_audit_log_with_description():
    log = (
        AuditLogBuilder()
        .set_actor(3)
        .set_entity("REQUEST", 7)
        .set_action("REJECTED")
        .set_description("No cumple política de gastos")
        .build()
    )
    assert log.description == "No cumple política de gastos"
