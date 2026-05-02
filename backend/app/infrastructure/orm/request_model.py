from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text        #type: ignore
from sqlalchemy.orm import relationship        #type: ignore
from datetime import datetime

from backend.app.infrastructure.database import Base
from backend.app.domain.enums import RequestStatus, ExpenseCategory


class RequestModel(Base):
    """Modelo ORM para Request."""
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    category = Column(Enum(ExpenseCategory), nullable=False)
    receipt_url = Column(String(500), nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.SUBMITTED, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    finance_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    employee = relationship("UserModel", foreign_keys=[employee_id], back_populates="requests")
    approvals = relationship("ApprovalModel", back_populates="request", cascade="all, delete-orphan")
    notifications = relationship("NotificationModel", back_populates="request")
    audit_logs = relationship("AuditLogModel", back_populates="request")

    def to_domain(self):
        """Convierte a entidad de dominio."""
        from backend.app.domain.entities.request import Request
        from backend.app.domain.states.submitted_state import SubmittedState
        from backend.app.domain.value_objects import Money, RequestTitle
        from backend.app.domain.enums import RequestStatus

        # Mapear estado a state object
        state_map = {
            RequestStatus.SUBMITTED: "SubmittedState",
            RequestStatus.MANAGER_REVIEW: "ManagerReviewState",
            RequestStatus.APPROVED: "ApprovedState",
            RequestStatus.REJECTED: "RejectedState",
        }

        return Request(
            id=self.id,
            employee_id=self.employee_id,
            title=RequestTitle(self.title),
            description=self.description or "",
            amount=Money(self.amount, self.currency),
            category=self.category,
            receipt_url=self.receipt_url,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            submitted_by_id=self.submitted_by_id,
            manager_id=self.manager_id,
            finance_id=self.finance_id,
        )


class ApprovalModel(Base):
    """Modelo ORM para Approval."""
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False, index=True)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approval_type = Column(String(50), nullable=False)  # MANAGER_REVIEW, FINANCE_REVIEW
    comment = Column(Text, nullable=True)
    approved_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("RequestModel", back_populates="approvals")

    def to_domain(self):
        """Convierte a entidad de dominio."""
        from backend.app.domain.entities.request import Approval
        return Approval(
            id=self.id,
            request_id=self.request_id,
            approver_id=self.approver_id,
            approval_type=self.approval_type,
            comment=self.comment,
            approved_at=self.approved_at,
        )


class AuditLogModel(Base):
    """Modelo ORM para AuditLog."""
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
        """Convierte a entidad de dominio."""
        from backend.app.domain.entities.audit_log import AuditLog
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


class NotificationModel(Base):
    """Modelo ORM para Notification."""
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
        """Convierte a entidad de dominio."""
        from backend.app.domain.entities.notification import Notification
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
