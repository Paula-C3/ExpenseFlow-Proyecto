from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class AuditLog:
    entity_type: str
    entity_id: int
    action: str
    id: int = 0
    actor_id: Optional[int] = None
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    description: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)