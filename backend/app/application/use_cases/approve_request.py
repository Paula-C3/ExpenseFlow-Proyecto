from datetime import datetime
from app.domain.interfaces.request_repository import IRequestRepository
from app.domain.interfaces.event_bus import IEventBus
from app.domain.enums import RoleType
from app.application.dtos.request_dto import ApproveRequestDTO, RequestResponseDTO
from app.domain.events import RequestApprovedEvent

ALLOWED_APPROVE_ROLES = {RoleType.MANAGER.value, RoleType.FINANCE_ADMIN.value, RoleType.SYSTEM_ADMIN.value}


class ApproveRequestUseCase:
    def __init__(self, repo: IRequestRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, request_id: int, dto: ApproveRequestDTO, approver_id: int, role: str) -> RequestResponseDTO:
        if role not in ALLOWED_APPROVE_ROLES:
            raise PermissionError("Solo MANAGER, FINANCE_ADMIN o SYSTEM_ADMIN pueden aprobar")

        request = self.repo.find_by_id(request_id)
        if not request:
            raise ValueError(f"Solicitud {request_id} no encontrada")

        request.approve(approver_id=approver_id, comment=dto.comment or "")
        updated = self.repo.update(request)

        self.event_bus.publish(RequestApprovedEvent(
            request_id=request_id,
            approver_id=approver_id,
            employee_id=request.employee_id,
            comment=dto.comment or "",
            timestamp=datetime.utcnow(),
        ))

        return RequestResponseDTO.from_domain(updated)