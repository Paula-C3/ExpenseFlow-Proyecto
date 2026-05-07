from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query        #type: ignore
from sqlalchemy.orm import Session                                  #type: ignore

from app.api.dependencies import get_current_user, require_role
from app.application.dtos.notification_dto import AuditLogDTO, NotificationDTO
from app.infrastructure.database import get_db
from app.infrastructure.orm.audit_log_repository import AuditLogRepository
from app.infrastructure.orm.notification_repository import NotificationRepository

router = APIRouter(tags=["notifications"])


@router.get("/notifications", response_model=List[NotificationDTO])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["sub"])
    repo = NotificationRepository(db)
    notifications = repo.find_by_user(user_id)
    return [NotificationDTO.from_domain(n) for n in notifications]


@router.patch("/notifications/{notification_id}/read", response_model=NotificationDTO)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = NotificationRepository(db)
    updated = repo.mark_as_read(notification_id)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Notificación {notification_id} no encontrada")
    return NotificationDTO.from_domain(updated)


@router.get("/audit", response_model=List[AuditLogDTO])
def get_audit_logs(
    request_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("SYSTEM_ADMIN")),
):
    repo = AuditLogRepository(db)
    if request_id is not None:
        logs = repo.find_by_entity(entity_type="request", entity_id=request_id)
    else:
        logs = repo.find_all()
    return [AuditLogDTO.from_domain(log) for log in logs]