from app.domain.states.request_state import RequestState
from app.domain.enums import RequestStatus


class ManagerReviewState(RequestState):
    """Estado: en revisión del manager."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.MANAGER_REVIEW

    def submit(self, request) -> None:
        raise Exception("No se puede re-enviar una solicitud en revisión")

    def approve(self, request, approver_id: int = 0, comment: str = "") -> None:
        from app.domain.states.approved_state import ApprovedState
        request.state = ApprovedState()
        request.status = RequestStatus.APPROVED

    def reject(self, request, rejector_id: int = 0, reason: str = "") -> None:
        from app.domain.states.rejected_state import RejectedState
        request.state = RejectedState()
        request.status = RequestStatus.REJECTED

    def complete(self, request) -> None:
        raise Exception("No se puede completar una solicitud en revisión de manager")
