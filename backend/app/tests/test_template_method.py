import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.application.patterns.template_method import ApproveRequestProcessor
from app.domain.enums import RoleType, ExpenseCategory, RequestStatus
from app.domain.value_objects import Money, RequestTitle
from app.domain.entities.request import Request


def make_request():
    return Request(
        id=1, employee_id=2,
        title=RequestTitle("Test"), amount=Money(100.0, "USD"),
        category=ExpenseCategory.OTHER, status=RequestStatus.SUBMITTED,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(), submitted_by_id=2,
    )


def test_all_steps_called_in_order():
    repo = MagicMock()
    event_bus = MagicMock()
    repo.update.return_value = make_request()

    processor = ApproveRequestProcessor(repo=repo, event_bus=event_bus)
    processor.process(make_request(), actor_id=5, role=RoleType.MANAGER.value)

    assert processor.steps_called == ["validate", "execute", "notify", "audit"]


def test_invalid_role_raises_before_execute():
    repo = MagicMock()
    event_bus = MagicMock()
    processor = ApproveRequestProcessor(repo=repo, event_bus=event_bus)

    with pytest.raises(PermissionError):
        processor.process(make_request(), actor_id=99, role=RoleType.EMPLOYEE.value)

    assert "execute" not in processor.steps_called
