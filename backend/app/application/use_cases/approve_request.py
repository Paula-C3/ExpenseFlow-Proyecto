from datetime import datetime

from backend.app.application.dtos.request_dto import ApproveRequestDTO, RequestResponseDTO
from backend.app.domain.enums import RequestStatus, RoleType
from backend.app.domain.events import RequestApprovedEvent, RequestStatusChangedEvent
from backend.app.domain.interfaces.event_bus import IEventBus
from backend.app.domain.interfaces.request_repository import IRequestRepository


ALLOWED_APPROVE_ROLES = {
    RoleType.MANAGER.value,
    RoleType.FINANCE_ANALYST.value,
    RoleType.FINANCE_ADMIN.value,
    RoleType.SYSTEM_ADMIN.value,
}


class ApproveRequestUseCase:
    def __init__(self, repo: IRequestRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(
        self,
        request_id: int,
        dto: ApproveRequestDTO,
        approver_id: int,
        role: str,
    ) -> RequestResponseDTO:
        if role not in ALLOWED_APPROVE_ROLES:
            raise PermissionError("Tu rol no puede aprobar solicitudes")

        request = self.repo.find_by_id(request_id)

        if not request:
            raise ValueError(f"Solicitud {request_id} no encontrada")

        if request.employee_id == approver_id:
            raise PermissionError("Un empleado no puede aprobar su propio gasto")

        if request.status in (
            RequestStatus.REJECTED,
            RequestStatus.CANCELLED,
            RequestStatus.PAID,
        ):
            raise PermissionError("Esta solicitud ya está cerrada")

        previous_status = request.status
        request.updated_at = datetime.utcnow()

        amount = float(request.amount.amount)

        if role == RoleType.MANAGER.value:
            if request.status != RequestStatus.MANAGER_REVIEW:
                raise PermissionError(
                    "El Manager solo puede aprobar solicitudes en MANAGER_REVIEW"
                )

            request.manager_id = approver_id
            request.status = RequestStatus.FINANCE_REVIEW

        elif role == RoleType.FINANCE_ANALYST.value:
            if request.status != RequestStatus.FINANCE_REVIEW:
                raise PermissionError(
                    "El Finance Analyst solo puede aprobar solicitudes en FINANCE_REVIEW"
                )

            request.finance_id = approver_id

            if amount > 500:
                request.status = RequestStatus.READY_FOR_PAYMENT
            else:
                request.status = RequestStatus.PAID

        elif role == RoleType.FINANCE_ADMIN.value:
            if request.status not in (
                RequestStatus.FINANCE_REVIEW,
                RequestStatus.READY_FOR_PAYMENT,
            ):
                raise PermissionError(
                    "El Finance Admin solo puede aprobar solicitudes en FINANCE_REVIEW o READY_FOR_PAYMENT"
                )

            request.finance_id = approver_id
            request.status = RequestStatus.PAID

        elif role == RoleType.SYSTEM_ADMIN.value:
            if request.status == RequestStatus.MANAGER_REVIEW:
                request.manager_id = approver_id
                request.status = RequestStatus.FINANCE_REVIEW

            elif request.status == RequestStatus.FINANCE_REVIEW:
                request.finance_id = approver_id

                if amount > 500:
                    request.status = RequestStatus.READY_FOR_PAYMENT
                else:
                    request.status = RequestStatus.PAID

            elif request.status == RequestStatus.READY_FOR_PAYMENT:
                request.finance_id = approver_id
                request.status = RequestStatus.PAID

            else:
                raise PermissionError(
                    f"No se puede aprobar una solicitud en estado {request.status.value}"
                )

        updated = self.repo.update(request)

        self.event_bus.publish(
            RequestApprovedEvent(
                request_id=request_id,
                approver_id=approver_id,
                employee_id=request.employee_id,
                comment=dto.comment or "",
                timestamp=datetime.utcnow(),
            )
        )

        self.event_bus.publish(
            RequestStatusChangedEvent(
                request_id=request_id,
                previous_status=previous_status,
                new_status=request.status,
                actor_id=approver_id,
                timestamp=datetime.utcnow(),
            )
        )

        return RequestResponseDTO.from_domain(updated)