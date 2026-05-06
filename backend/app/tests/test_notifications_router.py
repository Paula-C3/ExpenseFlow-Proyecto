from datetime import datetime
from unittest.mock import MagicMock, patch

from backend.app.domain.entities.notification import Notification


def make_notification(user_id: int, notif_id: int = 1) -> Notification:
    return Notification(
        id=notif_id,
        user_id=user_id,
        title="Solicitud aprobada",
        message="Tu solicitud fue aprobada.",
        notification_type="EXPENSE_APPROVED",
        reference_id=1,
        is_read=False,
        created_at=datetime.utcnow(),
    )


# --- GET /notifications ---

def test_get_notifications_no_token(client):
    response = client.get("/notifications")
    assert response.status_code == 403  # HTTPBearer returns 403 when no credentials are provided


def test_get_notifications_returns_only_current_user(employee_client):
    user_id = 1
    user_notif = make_notification(user_id=user_id, notif_id=1)

    with patch(
        "backend.app.api.routes.notifications_router.NotificationRepository"
    ) as MockRepo:
        MockRepo.return_value.find_by_user.return_value = [user_notif]

        response = employee_client.get("/notifications")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_id
    MockRepo.return_value.find_by_user.assert_called_once_with(user_id)


# --- PATCH /notifications/{id}/read ---

def test_mark_notification_as_read(employee_client):
    updated = make_notification(user_id=1, notif_id=1)
    updated.is_read = True

    with patch(
        "backend.app.api.routes.notifications_router.NotificationRepository"
    ) as MockRepo:
        MockRepo.return_value.mark_as_read.return_value = updated

        response = employee_client.patch("/notifications/1/read")

    assert response.status_code == 200
    assert response.json()["is_read"] is True


def test_mark_notification_as_read_not_found(employee_client):
    with patch(
        "backend.app.api.routes.notifications_router.NotificationRepository"
    ) as MockRepo:
        MockRepo.return_value.mark_as_read.return_value = None

        response = employee_client.patch("/notifications/999/read")

    assert response.status_code == 404


# --- GET /audit ---

def test_get_audit_logs_as_non_admin_returns_403(employee_client):
    response = employee_client.get("/audit")
    assert response.status_code == 403


def test_get_audit_logs_as_admin(admin_client):
    from backend.app.domain.entities.audit_log import AuditLog

    log = AuditLog(
        id=1,
        actor_id=1,
        entity_type="request",
        entity_id=1,
        action="APPROVED",
        timestamp=datetime.utcnow(),
    )

    with patch(
        "backend.app.api.routes.notifications_router.AuditLogRepository"
    ) as MockRepo:
        MockRepo.return_value.find_all.return_value = [log]

        response = admin_client.get("/audit")

    assert response.status_code == 200
    assert response.json()[0]["action"] == "APPROVED"


def test_get_audit_logs_filtered_by_request(admin_client):
    from backend.app.domain.entities.audit_log import AuditLog

    log = AuditLog(
        id=1,
        actor_id=1,
        entity_type="request",
        entity_id=5,
        action="REJECTED",
        timestamp=datetime.utcnow(),
    )

    with patch(
        "backend.app.api.routes.notifications_router.AuditLogRepository"
    ) as MockRepo:
        MockRepo.return_value.find_by_entity.return_value = [log]

        response = admin_client.get("/audit?request_id=5")

    assert response.status_code == 200
    MockRepo.return_value.find_by_entity.assert_called_once_with(entity_type="request", entity_id=5)