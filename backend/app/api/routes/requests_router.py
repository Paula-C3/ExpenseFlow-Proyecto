from typing import List

from fastapi import APIRouter, Depends, HTTPException       #type: ignore
from sqlalchemy.orm import Session                          #type: ignore

from backend.app.api.dependencies import get_current_user
from backend.app.application.dtos.request_dto import (
    ApproveRequestDTO,
    CreateRequestDTO,
    RejectRequestDTO,
    RequestResponseDTO,
)
from backend.app.application.use_cases.approve_request import ApproveRequestUseCase
from backend.app.application.use_cases.create_request import CreateRequestUseCase
from backend.app.application.use_cases.get_request_detail import GetRequestDetailUseCase
from backend.app.application.use_cases.get_requests_by_role import GetRequestsByRoleUseCase
from backend.app.application.use_cases.reject_request import RejectRequestUseCase
from backend.app.domain.factories.singleton import EventBusRegistry
from backend.app.infrastructure.database import get_db
from backend.app.infrastructure.orm.request_repository import SQLRequestRepository

router = APIRouter(prefix="/requests", tags=["requests"])


def get_event_bus():
    return EventBusRegistry().get_event_bus()


@router.post("", response_model=RequestResponseDTO, status_code=201)
def create_request(
    dto: CreateRequestDTO,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    employee_id = int(current_user["sub"])
    repo = SQLRequestRepository(db)
    event_bus = get_event_bus()
    use_case = CreateRequestUseCase(repo=repo, event_bus=event_bus)
    return use_case.execute(dto=dto, employee_id=employee_id)


@router.get("", response_model=List[RequestResponseDTO])
def get_requests(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    role = current_user["role"]
    employee_id = int(current_user["sub"])
    repo = SQLRequestRepository(db)
    use_case = GetRequestsByRoleUseCase(repo=repo)
    return use_case.execute(role=role, employee_id=employee_id)


@router.get("/{request_id}", response_model=RequestResponseDTO)
def get_request_detail(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = SQLRequestRepository(db)
    use_case = GetRequestDetailUseCase(repo=repo)
    try:
        return use_case.execute(request_id=request_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Solicitud {request_id} no encontrada")


@router.post("/{request_id}/approve", response_model=RequestResponseDTO)
def approve_request(
    request_id: int,
    dto: ApproveRequestDTO,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    approver_id = int(current_user["sub"])
    role = current_user["role"]
    repo = SQLRequestRepository(db)
    event_bus = get_event_bus()
    use_case = ApproveRequestUseCase(repo=repo, event_bus=event_bus)
    try:
        return use_case.execute(request_id=request_id, dto=dto, approver_id=approver_id, role=role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{request_id}/reject", response_model=RequestResponseDTO)
def reject_request(
    request_id: int,
    dto: RejectRequestDTO,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    rejector_id = int(current_user["sub"])
    role = current_user["role"]
    repo = SQLRequestRepository(db)
    event_bus = get_event_bus()
    use_case = RejectRequestUseCase(repo=repo, event_bus=event_bus)
    try:
        return use_case.execute(request_id=request_id, dto=dto, rejector_id=rejector_id, role=role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))