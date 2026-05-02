from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Notification:
    user_id: int
    title: str
    message: str
    notification_type: str
    id: int = 0
    reference_id: Optional[int] = None
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None