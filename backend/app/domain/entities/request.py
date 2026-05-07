from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.domain.enums import RequestStatus, ExpenseCategory


class Request:
    """Entidad de dominio para solicitud de gasto."""

    def __init__(
        self,
        employee_id: int,
        title,
        amount,
        category: "ExpenseCategory" = None,
        description: str = "",
        receipt_url: Optional[str] = None,
        state=None,
        status: "RequestStatus" = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        submitted_by_id: Optional[int] = None,
        manager_id: Optional[int] = None,
        finance_id: Optional[int] = None,
        id: Optional[int] = None,
        event_bus=None,
    ):
        self.id = id
        self.employee_id = employee_id
        self.title = title
        self.amount = amount
        self.category = category or ExpenseCategory.OTHER
        self.description = description
        self.receipt_url = receipt_url
        self.status = status or RequestStatus.SUBMITTED
        self.submitted_by_id = submitted_by_id
        self.manager_id = manager_id
        self.finance_id = finance_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.event_bus = event_bus

        if state is not None:
            self.state = state
        else:
            from app.domain.states.submitted_state import SubmittedState
            self.state = SubmittedState()

    def submit(self):
        self.state.submit(self)

    def approve(self, approver_id: Optional[int] = None, comment: str = ""):
        prev_status = self.status
        self.state.approve(self)
        if self.event_bus:
            from app.domain.events import RequestApprovedEvent, RequestStatusChangedEvent
            self.event_bus.publish(RequestApprovedEvent(
                request_id=self.id,
                approver_id=approver_id or self.manager_id or self.employee_id,
                comment=comment,
            ))
            self.event_bus.publish(RequestStatusChangedEvent(
                request_id=self.id,
                previous_status=prev_status,
                new_status=self.status,
                actor_id=approver_id or self.employee_id,
            ))

    def reject(self, rejector_id: Optional[int] = None, reason: str = ""):
        prev_status = self.status
        self.state.reject(self)
        if self.event_bus:
            from app.domain.events import RequestRejectedEvent, RequestStatusChangedEvent
            self.event_bus.publish(RequestRejectedEvent(
                request_id=self.id,
                rejector_id=rejector_id or self.employee_id,
                reason=reason,
            ))
            self.event_bus.publish(RequestStatusChangedEvent(
                request_id=self.id,
                previous_status=prev_status,
                new_status=self.status,
                actor_id=rejector_id or self.employee_id,
            ))

    def complete(self):
        self.state.complete(self)


@dataclass
class Approval:
    request_id: int
    approver_id: int
    approval_type: str
    comment: Optional[str] = None
    approved_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class AuditLog:
    actor_id: int
    entity_type: str
    entity_id: int
    action: str
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    description: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class Notification:
    user_id: int
    title: str
    message: str
    notification_type: str
    reference_id: Optional[int] = None
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None
    id: Optional[int] = None
