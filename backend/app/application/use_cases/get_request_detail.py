from backend.app.domain.interfaces.request_repository import IRequestRepository
from backend.app.application.dtos.request_dto import RequestResponseDTO


class GetRequestDetailUseCase:
    def __init__(self, repo: IRequestRepository):
        self.repo = repo

    def execute(self, request_id: int) -> RequestResponseDTO:
        request = self.repo.find_by_id(request_id)
        if not request:
            raise ValueError(f"Solicitud {request_id} no encontrada")
        return RequestResponseDTO.from_domain(request)
