from backend.app.domain.interfaces.request_repository import IRequestRepository
from backend.app.domain.interfaces.event_bus import IEventBus
from backend.app.domain.enums import RoleType
from backend.app.application.dtos.request_dto import RejectRequestDTO, RequestResponseDTO

ALLOWED_REJECT_ROLES = {RoleType.MANAGER.value, RoleType.FINANCE_ADMIN.value, RoleType.SYSTEM_ADMIN.value}


class RejectRequestUseCase:
    def __init__(self, repo: IRequestRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, request_id: int, dto: RejectRequestDTO, rejector_id: int, role: str) -> RequestResponseDTO:
        if role not in ALLOWED_REJECT_ROLES:
            raise PermissionError("Solo MANAGER, FINANCE_ADMIN o SYSTEM_ADMIN pueden rechazar")

        request = self.repo.find_by_id(request_id)
        if not request:
            raise ValueError(f"Solicitud {request_id} no encontrada")

        request.event_bus = self.event_bus
        request.reject(rejector_id=rejector_id, reason=dto.reason)
        updated = self.repo.update(request)
        return RequestResponseDTO.from_domain(updated)
