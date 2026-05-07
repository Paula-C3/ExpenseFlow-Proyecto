
from app.domain.interfaces.event_bus import IEventListener, DomainEvent
from app.domain.events import (
    RequestApprovedEvent,
    RequestRejectedEvent,
    RequestSubmittedEvent,
    RequestStatusChangedEvent,
)
from app.domain.factories.audit_log_builder import AuditLogBuilder


class AuditListener(IEventListener):
    """Listener que crea logs de auditoría."""

    def __init__(self, audit_repository):
        self.audit_repository = audit_repository

    def handle(self, event: DomainEvent) -> None:
        """Maneja eventos de cambio de estado."""

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
    """Listener que crea notificaciones."""

    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def handle(self, event: DomainEvent) -> None:
        """Maneja eventos para crear notificaciones."""

        from app.domain.entities.notification import Notification

        if isinstance(event, RequestSubmittedEvent):
            notification = Notification(
                user_id=event.submitted_by_id,
                title="Solicitud enviada",
                message="Tu solicitud ha sido enviada para revisión",
                notification_type="REQUEST_SUBMITTED",
                reference_id=event.request_id,
                created_at=event.timestamp,
            )
            self.notification_repository.save(notification)

        elif isinstance(event, RequestApprovedEvent):
            notification = Notification(
                user_id=event.employee_id,
                title="Solicitud aprobada",
                message=f"Tu solicitud {event.request_id} ha sido aprobada",
                notification_type="REQUEST_APPROVED",
                reference_id=event.request_id,
                created_at=event.timestamp,
            )
            self.notification_repository.save(notification)

        elif isinstance(event, RequestRejectedEvent):
            notification = Notification(
                user_id=event.employee_id,
                title="Solicitud rechazada",
                message=f"Tu solicitud {event.request_id} ha sido rechazada",
                notification_type="REQUEST_REJECTED",
                reference_id=event.request_id,
                created_at=event.timestamp,
            )
            self.notification_repository.save(notification)