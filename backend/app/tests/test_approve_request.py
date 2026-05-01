import pytest
from unittest.mock import MagicMock
from datetime import datetime
from backend.app.application.use_cases.approve_request import ApproveRequestUseCase
from backend.app.application.dtos.request_dto import ApproveRequestDTO
from backend.app.domain.enums import RoleType, ExpenseCategory, RequestStatus
from backend.app.domain.value_objects import Money, RequestTitle
from backend.app.domain.entities.request import Request


def _fake_request():
    return Request(
        id=1, employee_id=2,
        title=RequestTitle("Viaje"), amount=Money(200.0, "USD"),
        category=ExpenseCategory.TRAVEL, status=RequestStatus.SUBMITTED,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(), submitted_by_id=2,
    )


def test_approve_fails_for_employee():
    repo = MagicMock()
    event_bus = MagicMock()
    repo.find_by_id.return_value = _fake_request()

    use_case = ApproveRequestUseCase(repo=repo, event_bus=event_bus)
    with pytest.raises(PermissionError):
        use_case.execute(request_id=1, dto=ApproveRequestDTO(), approver_id=99, role=RoleType.EMPLOYEE.value)


def test_approve_fails_for_finance_analyst():
    repo = MagicMock()
    event_bus = MagicMock()
    repo.find_by_id.return_value = _fake_request()

    use_case = ApproveRequestUseCase(repo=repo, event_bus=event_bus)
    with pytest.raises(PermissionError):
        use_case.execute(request_id=1, dto=ApproveRequestDTO(), approver_id=99, role=RoleType.FINANCE_ANALYST.value)


def test_approve_succeeds_for_manager():
    repo = MagicMock()
    event_bus = MagicMock()
    fake = _fake_request()
    repo.find_by_id.return_value = fake
    repo.update.return_value = fake

    use_case = ApproveRequestUseCase(repo=repo, event_bus=event_bus)
    result = use_case.execute(request_id=1, dto=ApproveRequestDTO(comment="ok"), approver_id=5, role=RoleType.MANAGER.value)

    repo.update.assert_called_once()


def test_approve_raises_if_not_found():
    repo = MagicMock()
    event_bus = MagicMock()
    repo.find_by_id.return_value = None

    use_case = ApproveRequestUseCase(repo=repo, event_bus=event_bus)
    with pytest.raises(ValueError):
        use_case.execute(request_id=999, dto=ApproveRequestDTO(), approver_id=5, role=RoleType.MANAGER.value)
