from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum     #type: ignore
from sqlalchemy.orm import relationship     #type: ignore
from datetime import datetime

from backend.app.infrastructure.database import Base
from backend.app.domain.enums import RoleType


class RoleModel(Base):
    """Modelo ORM para Role."""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(RoleType), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("UserModel", back_populates="role")

    def to_domain(self):
        """Convierte a entidad de dominio."""
        from backend.app.domain.entities.user import Role
        return Role(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class UserModel(Base):
    """Modelo ORM para User."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = relationship("RoleModel", back_populates="users")
    requests = relationship("RequestModel", back_populates="employee")
    notifications = relationship("NotificationModel", back_populates="user")
    audit_logs = relationship("AuditLogModel", back_populates="actor")

    def to_domain(self):
        """Convierte a entidad de dominio."""
        from backend.app.domain.entities.user import User
        from backend.app.domain.value_objects import Email
        
        return User(
            id=self.id,
            email=Email(self.email),
            full_name=self.full_name,
            hashed_password=self.hashed_password,
            role_id=self.role_id,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_domain(user):
        """Crea modelo ORM desde entidad de dominio."""
        return UserModel(
            id=user.id,
            email=str(user.email) if user.email else "",
            full_name=user.full_name,
            hashed_password=user.hashed_password,
            role_id=user.role_id,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
