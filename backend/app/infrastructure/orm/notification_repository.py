from typing import Optional, List
from sqlalchemy.orm import Session          #type: ignore

from app.domain.entities.notification import Notification
from app.infrastructure.orm.request_model import NotificationModel


class NotificationRepository:
    """Repositorio para Notification."""

    def __init__(self, db: Session):
        self.db = db

    def save(self, notification: Notification) -> Notification:
        """Guarda una nueva notificación."""
        db_notif = NotificationModel(
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            notification_type=notification.notification_type,
            reference_id=notification.reference_id,
            is_read=notification.is_read,
            created_at=notification.created_at,
            read_at=notification.read_at,
        )
        self.db.add(db_notif)
        self.db.commit()
        self.db.refresh(db_notif)
        return db_notif.to_domain()

    def find_by_id(self, notif_id: int) -> Optional[Notification]:
        """Busca notificación por ID."""
        db_notif = self.db.query(NotificationModel).filter(NotificationModel.id == notif_id).first()
        return db_notif.to_domain() if db_notif else None

    def find_by_user(self, user_id: int) -> List[Notification]:
        """Busca notificaciones de un usuario."""
        db_notifs = self.db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id
        ).order_by(NotificationModel.created_at.desc()).all()
        return [n.to_domain() for n in db_notifs]

    def find_unread_by_user(self, user_id: int) -> List[Notification]:
        """Busca notificaciones no leídas de un usuario."""
        db_notifs = self.db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id,
            not NotificationModel.is_read
        ).all()
        return [n.to_domain() for n in db_notifs]

    def mark_as_read(self, notif_id: int) -> Optional[Notification]:
        """Marca una notificación como leída."""
        from datetime import datetime
        db_notif = self.db.query(NotificationModel).filter(NotificationModel.id == notif_id).first()
        if db_notif:
            db_notif.is_read = True
            db_notif.read_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_notif)
            return db_notif.to_domain()
        return None

    def find_all(self) -> List[Notification]:
        """Retorna todas las notificaciones."""
        db_notifs = self.db.query(NotificationModel).order_by(
            NotificationModel.created_at.desc()
        ).all()
        return [n.to_domain() for n in db_notifs]
