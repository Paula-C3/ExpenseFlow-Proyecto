from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationDTO(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    reference_id: Optional[int] = None
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, n) -> "NotificationDTO":
        return cls(
            id=n.id,
            user_id=n.user_id,
            title=n.title,
            message=n.message,
            notification_type=n.notification_type,
            reference_id=n.reference_id,
            is_read=n.is_read,
            created_at=n.created_at,
            read_at=n.read_at,
        )


class AuditLogDTO(BaseModel):
    id: int
    actor_id: Optional[int] = None
    entity_type: str
    entity_id: int
    action: str
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    description: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, log) -> "AuditLogDTO":
        return cls(
            id=log.id,
            actor_id=log.actor_id,
            entity_type=log.entity_type,
            entity_id=log.entity_id,
            action=log.action,
            previous_state=log.previous_state,
            new_state=log.new_state,
            description=log.description,
            timestamp=log.timestamp,
        )
