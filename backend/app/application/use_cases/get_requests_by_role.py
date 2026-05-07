from typing import List
from app.domain.interfaces.request_repository import IRequestRepository
from app.domain.enums import RoleType
from app.application.dtos.request_dto import RequestResponseDTO


class GetRequestsByRoleUseCase:
    def __init__(self, repo: IRequestRepository):
        self.repo = repo

    def execute(self, role: str, employee_id: int) -> List[RequestResponseDTO]:
        if role == RoleType.EMPLOYEE.value:
            requests = self.repo.find_by_employee(employee_id)
        else:
            requests = self.repo.find_by_role(RoleType(role))
        return [RequestResponseDTO.from_domain(r) for r in requests]
