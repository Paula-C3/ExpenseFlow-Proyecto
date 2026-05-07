from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.infrastructure.database import Base

from app.domain.entities.request import Request, Approval, AuditLog, Notification
from app.domain.enums import RequestStatus, ExpenseCategory
from app.domain.value_objects import Money

# States
from app.domain.states.submitted_state import SubmittedState
from app.domain.states.approved_state import ApprovedState
from app.domain.states.rejected_state import RejectedState
from app.domain.states.manager_review_state import ManagerReviewState


class RequestModel(Base):
    __tablename__ = "requests"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    category = Column(Enum(ExpenseCategory), nullable=False)
    receipt_url = Column(String(500), nullable=True)

    status = Column(Enum(RequestStatus), default=RequestStatus.DRAFT, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    submitted_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    finance_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relaciones
    employee = relationship("UserModel", foreign_keys=[employee_id], back_populates="requests")
    submitted_by = relationship("UserModel", foreign_keys=[submitted_by_id])
    manager = relationship("UserModel", foreign_keys=[manager_id])
    finance = relationship("UserModel", foreign_keys=[finance_id])

    approvals = relationship("ApprovalModel", back_populates="request", cascade="all, delete-orphan")
    notifications = relationship("NotificationModel", back_populates="request")
    audit_logs = relationship("AuditLogModel", back_populates="request")

    def to_domain(self):
        state_map = {
            RequestStatus.SUBMITTED: SubmittedState,
            RequestStatus.MANAGER_REVIEW: ManagerReviewState,
            RequestStatus.APPROVED: ApprovedState,
            RequestStatus.REJECTED: RejectedState,
        }

        state_class = state_map.get(self.status)
        state = state_class() if state_class else SubmittedState()

        return Request(
            id=self.id,
            employee_id=self.employee_id,
            title=self.title,
            amount=Money(self.amount) if self.amount is not None else Money(0.0),
            category=self.category,
            description=self.description or "",
            receipt_url=self.receipt_url,
            state=state,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            submitted_by_id=self.submitted_by_id,
            manager_id=self.manager_id,
            finance_id=self.finance_id,
        )


# =========================
# APPROVAL
# =========================
class ApprovalModel(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False, index=True)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approval_type = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    approved_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("RequestModel", back_populates="approvals")

    def to_domain(self):
        return Approval(
            id=self.id,
            request_id=self.request_id,
            approver_id=self.approver_id,
            approval_type=self.approval_type,
            comment=self.comment,
            approved_at=self.approved_at,
        )


# =========================
# AUDIT LOG
# =========================
class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False, index=True)
    action = Column(String(50), nullable=False)
    previous_state = Column(String(50), nullable=True)
    new_state = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=True)

    actor = relationship("UserModel", back_populates="audit_logs")
    request = relationship("RequestModel", back_populates="audit_logs")

    def to_domain(self):
        return AuditLog(
            id=self.id,
            actor_id=self.actor_id,
            entity_type=self.entity_type,
            entity_id=self.entity_id,
            action=self.action,
            previous_state=self.previous_state,
            new_state=self.new_state,
            description=self.description,
            timestamp=self.timestamp,
        )


# =========================
# NOTIFICATION
# =========================
class NotificationModel(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    reference_id = Column(Integer, nullable=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    read_at = Column(DateTime, nullable=True)

    user = relationship("UserModel", back_populates="notifications")
    request = relationship("RequestModel", back_populates="notifications")

    def to_domain(self):
        return Notification(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            message=self.message,
            notification_type=self.notification_type,
            reference_id=self.reference_id,
            is_read=self.is_read,
            created_at=self.created_at,
            read_at=self.read_at,
        )
