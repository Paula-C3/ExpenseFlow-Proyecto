from typing import Optional, List
from sqlalchemy.orm import Session      #type: ignore

from backend.app.domain.entities.request import Request
from backend.app.domain.interfaces.request_repository import IRequestRepository
from backend.app.domain.enums import RequestStatus, RoleType
from backend.app.infrastructure.orm.request_model import RequestModel


class SQLRequestRepository(IRequestRepository):
    """Implementación de IRequestRepository con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def save(self, request: Request) -> Request:
        """Guarda una nueva solicitud."""
        db_request = RequestModel(
            employee_id=request.employee_id,
            title=str(request.title) if request.title else "",
            description=request.description,
            amount=request.amount.amount if request.amount else 0.0,
            currency=request.amount.currency if request.amount else "USD",
            category=request.category,
            receipt_url=request.receipt_url,
            status=request.status,
            submitted_by_id=request.submitted_by_id,
            manager_id=request.manager_id,
            finance_id=request.finance_id,
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        request.id = db_request.id
        self.db.refresh(db_request)
        return db_request.to_domain()

    def find_by_id(self, request_id: int) -> Optional[Request]:
        """Busca solicitud por ID."""
        db_request = self.db.query(RequestModel).filter(RequestModel.id == request_id).first()
        return db_request.to_domain() if db_request else None

    def find_by_status(self, status: RequestStatus) -> List[Request]:
        """Encuentra solicitudes por estado."""
        db_requests = self.db.query(RequestModel).filter(RequestModel.status == status).all()
        return [req.to_domain() for req in db_requests]

    def find_by_employee(self, employee_id: int) -> List[Request]:
        """Encuentra solicitudes de un empleado."""
        db_requests = self.db.query(RequestModel).filter(
            RequestModel.employee_id == employee_id
        ).all()
        return [req.to_domain() for req in db_requests]

    def find_by_role(self, role: RoleType) -> List[Request]:
        """Encuentra solicitudes según el rol."""
        if role == RoleType.EMPLOYEE:
            return []
        elif role == RoleType.MANAGER:
            db_requests = self.db.query(RequestModel).filter(
                RequestModel.status.in_([
                    RequestStatus.SUBMITTED,
                    RequestStatus.MANAGER_REVIEW,
                ])
            ).all()
        elif role in [RoleType.FINANCE_ANALYST, RoleType.FINANCE_ADMIN]:
            db_requests = self.db.query(RequestModel).filter(
                RequestModel.status.in_([
                    RequestStatus.APPROVED,
                    RequestStatus.FINANCE_REVIEW,
                ])
            ).all()
        else:  # SYSTEM_ADMIN
            db_requests = self.db.query(RequestModel).all()
        
        return [req.to_domain() for req in db_requests]

    def find_all(self) -> List[Request]:
        """Retorna todas las solicitudes."""
        db_requests = self.db.query(RequestModel).all()
        return [req.to_domain() for req in db_requests]

    def update(self, request: Request) -> Request:
        """Actualiza una solicitud."""
        db_request = self.db.query(RequestModel).filter(RequestModel.id == request.id).first()
        if not db_request:
            raise ValueError(f"Solicitud {request.id} no encontrada")
        
        db_request.title = str(request.title) if request.title else db_request.title
        db_request.description = request.description
        db_request.amount = request.amount.amount if request.amount else db_request.amount
        db_request.category = request.category
        db_request.receipt_url = request.receipt_url
        db_request.status = request.status
        db_request.manager_id = request.manager_id
        db_request.finance_id = request.finance_id
        
        self.db.commit()
        self.db.refresh(db_request)
        return db_request.to_domain()

    def delete(self, request_id: int) -> None:
        """Elimina una solicitud."""
        db_request = self.db.query(RequestModel).filter(RequestModel.id == request_id).first()
        if db_request:
            self.db.delete(db_request)
            self.db.commit()
