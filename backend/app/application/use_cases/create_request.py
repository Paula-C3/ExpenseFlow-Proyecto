from backend.app.application.dtos.request_dto import CreateRequestDTO, RequestResponseDTO
from backend.app.domain.enums import RequestStatus
from backend.app.domain.events import RequestCreatedEvent, RequestStatusChangedEvent
from backend.app.domain.factories.request_factory import RequestFactory
from backend.app.domain.interfaces.event_bus import IEventBus
from backend.app.domain.interfaces.request_repository import IRequestRepository


class CreateRequestUseCase:
    def __init__(self, repo: IRequestRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, dto: CreateRequestDTO, employee_id: int) -> RequestResponseDTO:
        if dto.amount <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        receipt_url = dto.receipt_url.strip() if dto.receipt_url else None

        request = RequestFactory.create(
            employee_id=employee_id,
            title=dto.title,
            amount=dto.amount,
            category=dto.category,
            description=dto.description or "",
            receipt_url=receipt_url,
        )

        previous_status = request.status

        if not receipt_url:
            request.status = RequestStatus.CHANGES_REQUESTED
        elif dto.amount <= 50:
            request.status = RequestStatus.FINANCE_REVIEW
        else:
            request.status = RequestStatus.MANAGER_REVIEW

        saved = self.repo.save(request)

        self.event_bus.publish(
            RequestCreatedEvent(
                request_id=saved.id,
                employee_id=employee_id,
                title=dto.title,
                amount=dto.amount,
            )
        )

        if saved.status == RequestStatus.CHANGES_REQUESTED:
            self.event_bus.publish(
                RequestStatusChangedEvent(
                    request_id=saved.id,
                    previous_status=previous_status,
                    new_status=saved.status,
                    actor_id=employee_id,
                )
            )

        return RequestResponseDTO.from_domain(saved)