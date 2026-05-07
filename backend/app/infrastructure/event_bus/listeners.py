from app.domain.interfaces.event_bus import IEventListener, DomainEvent
from app.domain.events import (
    RequestApprovedEvent,
    RequestCreatedEvent,
    RequestRejectedEvent,
    RequestSubmittedEvent,
    RequestStatusChangedEvent,
)
from app.domain.factories.audit_log_builder import AuditLogBuilder
from app.domain.entities.notification import Notification
from app.domain.enums import RoleType, RequestStatus
from app.infrastructure.orm.user_model import UserModel


class AuditListener(IEventListener):
    def __init__(self, audit_repository):
        self.audit_repository = audit_repository

    def handle(self, event: DomainEvent) -> None:
        if isinstance(event, RequestStatusChangedEvent):
            builder = AuditLogBuilder()
            audit_log = (
                builder
                .set_actor(event.actor_id)
                .set_entity("REQUEST", event.request_id)
                .set_action("STATUS_CHANGED")
                .set_state_transition(
                    event.previous_status.value,
                    event.new_status.value
                )
                .set_timestamp(event.timestamp)
                .build()
            )
            self.audit_repository.save(audit_log)

        elif isinstance(event, RequestApprovedEvent):
            builder = AuditLogBuilder()
            audit_log = (
                builder
                .set_actor(event.approver_id)
                .set_entity("REQUEST", event.request_id)
                .set_action("APPROVED")
                .set_description(event.comment)
                .set_timestamp(event.timestamp)
                .build()
            )
            self.audit_repository.save(audit_log)

        elif isinstance(event, RequestRejectedEvent):
            builder = AuditLogBuilder()
            audit_log = (
                builder
                .set_actor(event.rejector_id)
                .set_entity("REQUEST", event.request_id)
                .set_action("REJECTED")
                .set_description(event.reason)
                .set_timestamp(event.timestamp)
                .build()
            )
            self.audit_repository.save(audit_log)


class NotificationListener(IEventListener):
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository
        self.db = notification_repository.db

    def _users_by_role(self, role: RoleType):
        return (
            self.db.query(UserModel)
            .join(UserModel.role)
            .filter(UserModel.role.has(name=role))
            .all()
        )

    def _notify(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str,
        request_id: int,
        created_at,
    ):
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            reference_id=request_id,
            created_at=created_at,
        )
        self.notification_repository.save(notification)

    def _notify_role(
        self,
        role: RoleType,
        title: str,
        message: str,
        notification_type: str,
        request_id: int,
        created_at,
    ):
        users = self._users_by_role(role)

        for user in users:
            self._notify(
                user_id=user.id,
                title=title,
                message=message,
                notification_type=notification_type,
                request_id=request_id,
                created_at=created_at,
            )

    def handle(self, event: DomainEvent) -> None:
        if isinstance(event, RequestCreatedEvent):
            if event.amount <= 50:
                self._notify_role(
                    role=RoleType.FINANCE_ANALYST,
                    title="Solicitud lista para revisión financiera",
                    message=f"La solicitud {event.request_id} es menor o igual a 50 USD y requiere revisión de Finanzas.",
                    notification_type="FINANCE_REVIEW_REQUIRED",
                    request_id=event.request_id,
                    created_at=event.timestamp,
                )

                self._notify_role(
                    role=RoleType.FINANCE_ADMIN,
                    title="Solicitud lista para revisión financiera",
                    message=f"La solicitud {event.request_id} es menor o igual a 50 USD y puede ser revisada por Finanzas.",
                    notification_type="FINANCE_REVIEW_REQUIRED",
                    request_id=event.request_id,
                    created_at=event.timestamp,
                )

            else:
                self._notify_role(
                    role=RoleType.MANAGER,
                    title="Solicitud requiere aprobación de Manager",
                    message=f"La solicitud {event.request_id} requiere aprobación de Manager.",
                    notification_type="MANAGER_APPROVAL_REQUIRED",
                    request_id=event.request_id,
                    created_at=event.timestamp,
                )

        elif isinstance(event, RequestSubmittedEvent):
            self._notify(
                user_id=event.submitted_by_id,
                title="Solicitud enviada",
                message="Tu solicitud ha sido enviada para revisión.",
                notification_type="REQUEST_SUBMITTED",
                request_id=event.request_id,
                created_at=event.timestamp,
            )

        elif isinstance(event, RequestApprovedEvent):
            self._notify(
                user_id=event.employee_id,
                title="Solicitud aprobada",
                message=f"Tu solicitud {event.request_id} ha avanzado en el flujo de aprobación.",
                notification_type="REQUEST_APPROVED",
                request_id=event.request_id,
                created_at=event.timestamp,
            )

        elif isinstance(event, RequestRejectedEvent):
            self._notify(
                user_id=event.employee_id,
                title="Solicitud rechazada",
                message=f"Tu solicitud {event.request_id} ha sido rechazada.",
                notification_type="REQUEST_REJECTED",
                request_id=event.request_id,
                created_at=event.timestamp,
            )

        elif isinstance(event, RequestStatusChangedEvent):
            if event.new_status == RequestStatus.FINANCE_REVIEW:
                self._notify_role(
                    role=RoleType.FINANCE_ANALYST,
                    title="Solicitud lista para revisión financiera",
                    message=f"La solicitud {event.request_id} fue aprobada por Manager y ahora requiere revisión de Finanzas.",
                    notification_type="FINANCE_REVIEW_REQUIRED",
                    request_id=event.request_id,
                    created_at=event.timestamp,
                )

                self._notify_role(
                    role=RoleType.FINANCE_ADMIN,
                    title="Solicitud lista para revisión financiera",
                    message=f"La solicitud {event.request_id} está disponible para revisión financiera.",
                    notification_type="FINANCE_REVIEW_REQUIRED",
                    request_id=event.request_id,
                    created_at=event.timestamp,
                )

            elif event.new_status == RequestStatus.READY_FOR_PAYMENT:
                self._notify_role(
                    role=RoleType.FINANCE_ADMIN,
                    title="Solicitud lista para pago",
                    message=f"La solicitud {event.request_id} está lista para revisión final o pago.",
                    notification_type="REQUEST_READY_FOR_PAYMENT",
                    request_id=event.request_id,
                    created_at=event.timestamp,
                )
