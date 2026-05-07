import pytest

from app.domain.factories.request_factory import RequestFactory
from app.domain.enums import RequestStatus, ExpenseCategory


def test_request_factory_create():
    """Test: RequestFactory.create retorna objeto con status=SUBMITTED."""
    request = RequestFactory.create(
        employee_id=1,
        title="Pasaje de avión",
        amount=500.0,
        category=ExpenseCategory.TRAVEL,
        description="Viaje a conferencia",
    )
    
    assert request.status == RequestStatus.SUBMITTED
    assert request.employee_id == 1
    assert str(request.title) == "Pasaje de avión"
    assert request.amount.amount == 500.0
    assert request.category == ExpenseCategory.TRAVEL


def test_request_factory_invalid_title():
    """Test: Factory con título vacío lanza excepción."""
    with pytest.raises(ValueError):
        RequestFactory.create(
            employee_id=1,
            title="",
            amount=500.0,
        )


def test_request_factory_invalid_amount():
    """Test: Factory con monto negativo lanza excepción."""
    with pytest.raises(ValueError):
        RequestFactory.create(
            employee_id=1,
            title="Gasto válido",
            amount=-100.0,
        )


def test_request_factory_from_dict():
    """Test: crear desde diccionario."""
    data = {
        "employee_id": 2,
        "title": "Herramientas",
        "amount": 250.0,
        "category": "TOOLS",
        "description": "Licencia de software",
        "receipt_url": "http://example.com/receipt.pdf",
    }
    
    request = RequestFactory.create_from_dict(data)
    
    assert request.employee_id == 2
    assert str(request.title) == "Herramientas"
    assert request.amount.amount == 250.0
    assert request.receipt_url == "http://example.com/receipt.pdf"
    assert request.status == RequestStatus.SUBMITTED

