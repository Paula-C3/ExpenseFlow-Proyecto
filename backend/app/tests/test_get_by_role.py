from unittest.mock import MagicMock
from datetime import datetime
from app.application.use_cases.get_requests_by_role import GetRequestsByRoleUseCase
from app.domain.enums import RoleType, ExpenseCategory, RequestStatus
from app.domain.value_objects import Money, RequestTitle
from app.domain.entities.request import Request


def make_request(i):
    return Request(
        id=i, employee_id=1,
        title=RequestTitle(f"Solicitud {i}"), amount=Money(100.0 * i, "USD"),
        category=ExpenseCategory.OTHER, status=RequestStatus.SUBMITTED,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(), submitted_by_id=1,
    )


def test_employee_sees_own_requests():
    repo = MagicMock()
    repo.find_by_employee.return_value = [make_request(i) for i in range(1, 4)]

    result = GetRequestsByRoleUseCase(repo=repo).execute(role=RoleType.EMPLOYEE.value, employee_id=1)

    assert len(result) == 3
    repo.find_by_employee.assert_called_once_with(1)


def test_manager_sees_all_submitted():
    repo = MagicMock()
    repo.find_by_role.return_value = [make_request(1), make_request(2)]

    result = GetRequestsByRoleUseCase(repo=repo).execute(role=RoleType.MANAGER.value, employee_id=99)

    assert len(result) == 2
    repo.find_by_role.assert_called_once()


def test_empty_list_returned_when_no_requests():
    repo = MagicMock()
    repo.find_by_employee.return_value = []

    result = GetRequestsByRoleUseCase(repo=repo).execute(role=RoleType.EMPLOYEE.value, employee_id=1)
    assert result == []

