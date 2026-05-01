from datetime import datetime
from typing import Optional

from backend.app.domain.entities.request import AuditLog


class AuditLogBuilder:
    """Builder para crear AuditLog."""

    def __init__(self):
        self._actor_id: Optional[int] = None
        self._entity_type: str = ""
        self._entity_id: Optional[int] = None
        self._action: str = ""
        self._previous_state: Optional[str] = None
        self._new_state: Optional[str] = None
        self._description: Optional[str] = None
        self._timestamp: datetime = datetime.utcnow()

    def set_actor(self, actor_id: int) -> "AuditLogBuilder":
        """Establece el actor que realiza la acción."""
        self._actor_id = actor_id
        return self

    def set_entity(self, entity_type: str, entity_id: int) -> "AuditLogBuilder":
        """Establece la entidad afectada."""
        self._entity_type = entity_type
        self._entity_id = entity_id
        return self

    def set_action(self, action: str) -> "AuditLogBuilder":
        """Establece la acción realizada."""
        self._action = action
        return self

    def set_state_transition(
        self, previous_state: str, new_state: str
    ) -> "AuditLogBuilder":
        """Establece la transición de estado."""
        self._previous_state = previous_state
        self._new_state = new_state
        return self

    def set_description(self, description: str) -> "AuditLogBuilder":
        """Establece una descripción adicional."""
        self._description = description
        return self

    def set_timestamp(self, timestamp: datetime) -> "AuditLogBuilder":
        """Establece el timestamp (por defecto es ahora)."""
        self._timestamp = timestamp
        return self

    def build(self) -> AuditLog:
        """Construye el AuditLog."""
        if not self._actor_id:
            raise ValueError("actor_id es requerido")
        if not self._entity_type:
            raise ValueError("entity_type es requerido")
        if not self._entity_id:
            raise ValueError("entity_id es requerido")
        if not self._action:
            raise ValueError("action es requerida")

        return AuditLog(
            actor_id=self._actor_id,
            entity_type=self._entity_type,
            entity_id=self._entity_id,
            action=self._action,
            previous_state=self._previous_state,
            new_state=self._new_state,
            description=self._description,
            timestamp=self._timestamp,
        )
