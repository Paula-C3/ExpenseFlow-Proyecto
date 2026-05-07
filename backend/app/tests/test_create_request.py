from unittest.mock import MagicMock
from datetime import datetime
from app.application.use_cases.create_request import CreateRequestUseCase
from app.application.dtos.request_dto import CreateRequestDTO
from app.domain.enums import ExpenseCategory, RequestStatus
from app.domain.value_objects import Money, RequestTitle
from app.domain.entities.request import Request


def _fake_saved_request():
    return Request(
        id=1,
        employee_id=1,
        title=RequestTitle("Compra laptop"),
        amount=Money(500.0, "USD"),
        category=ExpenseCategory.TOOLS,
        status=RequestStatus.SUBMITTED,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        submitted_by_id=1,
    )


def test_create_request_calls_save_and_publish():
    repo = MagicMock()
    event_bus = MagicMock()
    repo.save.return_value = _fake_saved_request()

    use_case = CreateRequestUseCase(repo=repo, event_bus=event_bus)
    dto = CreateRequestDTO(title="Compra laptop", amount=500.0, category=ExpenseCategory.TOOLS)

    result = use_case.execute(dto=dto, employee_id=1)

    repo.save.assert_called_once()
    event_bus.publish.assert_called_once()
    assert result.status == RequestStatus.SUBMITTED
    assert result.employee_id == 1


def test_create_request_returns_dto_with_correct_fields():
    repo = MagicMock()
    event_bus = MagicMock()
    repo.save.return_value = _fake_saved_request()

    use_case = CreateRequestUseCase(repo=repo, event_bus=event_bus)
    dto = CreateRequestDTO(title="Compra laptop", amount=500.0, category=ExpenseCategory.TOOLS)
    result = use_case.execute(dto=dto, employee_id=1)

    assert result.amount == 500.0
    assert result.currency == "USD"
    assert result.category == ExpenseCategory.TOOLS
