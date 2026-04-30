from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta
import os

from backend.app.infrastructure.database import get_db
from backend.app.infrastructure.orm.user_model import UserModel
from backend.app.domain.enums import RoleType

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


def create_access_token(email: str, user_id: int, role: str, expires_delta: timedelta = None):
    """Crea un token JWT."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    payload = {
        "email": email,
        "user_id": user_id,
        "role": role,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    """Decodifica un token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        
        if email is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        return {"email": email, "user_id": user_id, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Obtiene el usuario actual desde el JWT."""
    token = credentials.credentials
    payload = decode_token(token)
    
    user = db.query(UserModel).filter(UserModel.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": payload["role"],
        "role_id": user.role_id,
    }


def require_role(*allowed_roles: str):
    """Middleware para verificar roles."""
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso",
            )
        return current_user
    return role_checker


def get_current_admin(current_user: dict = Depends(require_role("SYSTEM_ADMIN"))):
    """Verifica que sea admin."""
    return current_user


def get_current_approver(
    current_user: dict = Depends(
        require_role("MANAGER", "FINANCE_ADMIN", "SYSTEM_ADMIN")
    )
):
    """Verifica que sea approver."""
    return current_user
