from unittest.mock import MagicMock, patch

from backend.app.application.dtos.request_dto import RequestResponseDTO
from backend.app.domain.enums import ExpenseCategory, RequestStatus


def make_response_dto(**kwargs) -> dict:
    from datetime import datetime
    defaults = {
        "id": 1,
        "employee_id": 1,
        "title": "Taxi al aeropuerto",
        "description": "Viaje de trabajo",
        "amount": 30.0,
        "currency": "USD",
        "category": ExpenseCategory.TRANSPORTATION,
        "receipt_url": "http://example.com/receipt.pdf",
        "status": RequestStatus.DRAFT,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "manager_id": None,
        "finance_id": None,
    }
    defaults.update(kwargs)
    return defaults


# --- POST /requests ---

def test_create_request_no_token(client):
    response = client.post("/requests", json={
        "title": "Taxi",
        "amount": 30.0,
        "category": "TRANSPORTATION",
        "description": "Viaje",
    })
    assert response.status_code in (401, 403)


def test_create_request_as_employee(employee_client):
    mock_result = RequestResponseDTO(**make_response_dto())

    with patch("backend.app.api.routes.requests_router.get_event_bus", return_value=MagicMock()), \
         patch("backend.app.api.routes.requests_router.CreateRequestUseCase") as MockUseCase:
        MockUseCase.return_value.execute.return_value = mock_result

        response = employee_client.post("/requests", json={
            "title": "Taxi al aeropuerto",
            "amount": 30.0,
            "category": "TRANSPORTATION",
            "description": "Viaje de trabajo",
        })

    assert response.status_code == 201
    assert response.json()["title"] == "Taxi al aeropuerto"



# --- POST /requests/{id}/approve ---

def test_approve_request_as_employee_returns_403(employee_client):
    with patch("backend.app.api.routes.requests_router.get_event_bus", return_value=MagicMock()), \
         patch("backend.app.api.routes.requests_router.ApproveRequestUseCase") as MockUseCase:
        MockUseCase.return_value.execute.side_effect = PermissionError(
            "Solo MANAGER, FINANCE_ADMIN o SYSTEM_ADMIN pueden aprobar"
        )

        response = employee_client.post("/requests/1/approve", json={"comment": ""})

    assert response.status_code == 403

# --- GET /requests ---

def test_get_requests_no_token(client):
    response = client.get("/requests")
    assert response.status_code in (401, 403)


def test_get_requests_as_employee(employee_client):
    mock_result = [RequestResponseDTO(**make_response_dto())]

    with patch("app.api.routes.requests_router.GetRequestsByRoleUseCase") as MockUseCase:
        MockUseCase.return_value.execute.return_value = mock_result

        response = employee_client.get("/requests")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --- GET /requests/{id} ---

def test_get_request_detail_not_found(employee_client):
    with patch("app.api.routes.requests_router.GetRequestDetailUseCase") as MockUseCase:
        MockUseCase.return_value.execute.side_effect = ValueError("Solicitud 999 no encontrada")

        response = employee_client.get("/requests/999")

    assert response.status_code == 404