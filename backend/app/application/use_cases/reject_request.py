from datetime import datetime

from app.application.dtos.request_dto import RejectRequestDTO, RequestResponseDTO
from app.domain.enums import RequestStatus, RoleType
from app.domain.events import RequestRejectedEvent, RequestStatusChangedEvent
from app.domain.interfaces.event_bus import IEventBus
from app.domain.interfaces.request_repository import IRequestRepository


ALLOWED_REJECT_ROLES = {
    RoleType.MANAGER.value,
    RoleType.FINANCE_ANALYST.value,
    RoleType.FINANCE_ADMIN.value,
    RoleType.SYSTEM_ADMIN.value,
}


class RejectRequestUseCase:
    def __init__(self, repo: IRequestRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(
        self,
        request_id: int,
        dto: RejectRequestDTO,
        rejector_id: int,
        role: str,
    ) -> RequestResponseDTO:
        if role not in ALLOWED_REJECT_ROLES:
            raise PermissionError("Tu rol no puede rechazar solicitudes")

        request = self.repo.find_by_id(request_id)

        if not request:
            raise ValueError(f"Solicitud {request_id} no encontrada")

        if request.employee_id == rejector_id:
            raise PermissionError("Un empleado no puede rechazar su propio gasto")

        if request.status in (
            RequestStatus.REJECTED,
            RequestStatus.CANCELLED,
            RequestStatus.PAID,
        ):
            raise PermissionError("Esta solicitud ya está cerrada")

        if role == RoleType.MANAGER.value:
            if request.status != RequestStatus.MANAGER_REVIEW:
                raise PermissionError(
                    "El Manager solo puede rechazar solicitudes en MANAGER_REVIEW"
                )

        elif role == RoleType.FINANCE_ANALYST.value:
            if request.status != RequestStatus.FINANCE_REVIEW:
                raise PermissionError(
                    "El Finance Analyst solo puede rechazar solicitudes en FINANCE_REVIEW"
                )

        elif role == RoleType.FINANCE_ADMIN.value:
            if request.status not in (
                RequestStatus.FINANCE_REVIEW,
                RequestStatus.READY_FOR_PAYMENT,
            ):
                raise PermissionError(
                    "El Finance Admin solo puede rechazar solicitudes en FINANCE_REVIEW o READY_FOR_PAYMENT"
                )

        previous_status = request.status
        request.status = RequestStatus.REJECTED
        request.updated_at = datetime.utcnow()

        updated = self.repo.update(request)

        self.event_bus.publish(
            RequestRejectedEvent(
                request_id=request_id,
                rejector_id=rejector_id,
                employee_id=request.employee_id,
                reason=dto.reason,
                timestamp=datetime.utcnow(),
            )
        )

        self.event_bus.publish(
            RequestStatusChangedEvent(
                request_id=request_id,
                previous_status=previous_status,
                new_status=RequestStatus.REJECTED,
                actor_id=rejector_id,
                timestamp=datetime.utcnow(),
            )
        )

        return RequestResponseDTO.from_domain(updated)
