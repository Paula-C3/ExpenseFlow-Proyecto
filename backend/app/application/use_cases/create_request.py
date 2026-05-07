from backend.app.domain.interfaces.request_repository import IRequestRepository
from backend.app.domain.interfaces.event_bus import IEventBus
from backend.app.domain.factories.request_factory import RequestFactory
from backend.app.domain.events import RequestCreatedEvent
from backend.app.application.dtos.request_dto import CreateRequestDTO, RequestResponseDTO
from backend.app.domain.enums import RequestStatus


class CreateRequestUseCase:
    def __init__(self, repo: IRequestRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, dto: CreateRequestDTO, employee_id: int) -> RequestResponseDTO:
        request = RequestFactory.create(
            employee_id=employee_id,
            title=dto.title,
            amount=dto.amount,
            category=dto.category,
            description=dto.description or "",
            receipt_url=dto.receipt_url,
        )

        if dto.amount <= 50:
            request.status = RequestStatus.FINANCE_REVIEW
        elif dto.amount <= 500:
            request.status = RequestStatus.MANAGER_REVIEW
        else:
            request.status = RequestStatus.MANAGER_REVIEW

        saved = self.repo.save(request)

        self.event_bus.publish(RequestCreatedEvent(
            request_id=saved.id,
            employee_id=employee_id,
            title=dto.title,
            amount=dto.amount,
        ))

        return RequestResponseDTO.from_domain(saved)