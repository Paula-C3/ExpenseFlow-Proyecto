from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from backend.app.domain.enums import RoleType
from backend.app.domain.value_objects import Email


@dataclass
class Role:
    """Entidad Role."""
    id: Optional[int] = None
    name: RoleType = RoleType.EMPLOYEE
    description: Optional[str] = None

    def __repr__(self) -> str:
        return f"Role(id={self.id}, name={self.name.value})"


@dataclass
class User:
    """Entidad User pura (sin ORM)."""
    id: Optional[int] = None
    email: Optional[Email] = None
    full_name: str = ""
    hashed_password: str = ""
    role_id: Optional[int] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, full_name={self.full_name})"

    @property
    def email_str(self) -> str:
        """Retorna email como string."""
        return str(self.email) if self.email else ""
