from typing import Optional, List
from sqlalchemy.orm import Session          #type: ignore

from app.domain.entities.audit_log import AuditLog
from app.infrastructure.orm.request_model import AuditLogModel


class AuditLogRepository:
    """Repositorio para AuditLog."""

    def __init__(self, db: Session):
        self.db = db

    def save(self, audit_log: AuditLog) -> AuditLog:
        """Guarda un nuevo log de auditoría."""
        db_log = AuditLogModel(
            actor_id=audit_log.actor_id,
            entity_type=audit_log.entity_type,
            entity_id=audit_log.entity_id,
            action=audit_log.action,
            previous_state=audit_log.previous_state,
            new_state=audit_log.new_state,
            description=audit_log.description,
            timestamp=audit_log.timestamp,
        )
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log.to_domain()

    def find_by_id(self, log_id: int) -> Optional[AuditLog]:
        """Busca log por ID."""
        db_log = self.db.query(AuditLogModel).filter(AuditLogModel.id == log_id).first()
        return db_log.to_domain() if db_log else None

    def find_by_entity(self, entity_type: str, entity_id: int) -> List[AuditLog]:
        """Busca logs por entidad."""
        db_logs = self.db.query(AuditLogModel).filter(
            AuditLogModel.entity_type == entity_type,
            AuditLogModel.entity_id == entity_id,
        ).all()
        return [log.to_domain() for log in db_logs]

    def find_all(self) -> List[AuditLog]:
        """Retorna todos los logs."""
        db_logs = self.db.query(AuditLogModel).order_by(AuditLogModel.timestamp.desc()).all()
        return [log.to_domain() for log in db_logs]
