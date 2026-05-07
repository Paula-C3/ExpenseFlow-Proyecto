import pytest
from pydantic import ValidationError
from backend.app.application.dtos.request_dto import CreateRequestDTO, RejectRequestDTO
from backend.app.domain.enums import ExpenseCategory


def test_create_request_dto_valid():
    dto = CreateRequestDTO(title="Compra laptop", amount=500.0, category=ExpenseCategory.TOOLS)
    assert dto.title == "Compra laptop"
    assert dto.amount == 500.0


def test_create_request_dto_missing_title():
    with pytest.raises(ValidationError):
        CreateRequestDTO(amount=500.0, category=ExpenseCategory.TOOLS)


def test_create_request_dto_negative_amount():
    with pytest.raises(ValidationError):
        CreateRequestDTO(title="Test", amount=-10.0, category=ExpenseCategory.TOOLS)


def test_create_request_dto_zero_amount():
    with pytest.raises(ValidationError):
        CreateRequestDTO(title="Test", amount=0.0, category=ExpenseCategory.TOOLS)


def test_reject_dto_requires_reason():
    with pytest.raises(ValidationError):
        RejectRequestDTO(reason="")


def test_reject_dto_valid():
    dto = RejectRequestDTO(reason="No cumple política")
    assert dto.reason == "No cumple política"
