from fastapi import APIRouter, Depends, HTTPException, status        #type: ignore
from sqlalchemy.orm import Session                                   #type: ignore

from backend.app.api.schemas.auth_schemas import UserLogin, UserRegister, TokenResponse
from backend.app.api.dependencies import create_access_token, get_current_user
from backend.app.infrastructure.database import get_db
from backend.app.infrastructure.orm.user_model import UserModel, RoleModel
from backend.app.infrastructure.security import hash_password, verify_password
from backend.app.domain.enums import RoleType

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login de usuario.
    
    Returns:
        - access_token: Token JWT
        - token_type: Tipo de token (bearer)
        - role: Rol del usuario
        - user_id: ID del usuario
    """
    user = db.query(UserModel).filter(UserModel.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    # Obtener el rol del usuario
    role = db.query(RoleModel).filter(RoleModel.id == user.role_id).first()
    role_name = role.name.value if role else "EMPLOYEE"
    
    # Crear token
    access_token = create_access_token(
        email=user.email,
        user_id=user.id,
        role=role_name,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_name,
        "user_id": user.id,
    }


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registro de nuevo usuario.
    
    El usuario se registra con rol por defecto EMPLOYEE.
    """
    # Verificar que no existe el email
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado",
        )
    
    # Obtener o crear rol EMPLOYEE
    role = db.query(RoleModel).filter(RoleModel.name == RoleType.EMPLOYEE).first()
    if not role:
        role = RoleModel(name=RoleType.EMPLOYEE, description="Empleado")
        db.add(role)
        db.commit()
        db.refresh(role)
    
    # Crear usuario
    new_user = UserModel(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role_id=role.id,
        is_active=True,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Crear token
    access_token = create_access_token(
        email=new_user.email,
        user_id=new_user.id,
        role=RoleType.EMPLOYEE.value,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": RoleType.EMPLOYEE.value,
        "user_id": new_user.id,
    }


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Obtiene información del usuario autenticado."""
    return current_user


@router.get("/users")
async def list_users(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lista todos los usuarios (solo ADMIN)."""
    if current_user["role"] != "SYSTEM_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden listar usuarios",
        )
    
    users = db.query(UserModel).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role_id": u.role_id,
            "is_active": u.is_active,
        }
        for u in users
    ]
