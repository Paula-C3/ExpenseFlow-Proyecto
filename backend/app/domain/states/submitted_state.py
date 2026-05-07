from app.domain.states.request_state import RequestState
from app.domain.enums import RequestStatus


class SubmittedState(RequestState):

    def submit(self, request):
        raise Exception("Already submitted")

    def approve(self, request):
        from app.domain.states.approved_state import ApprovedState
        request.state = ApprovedState()
        request.status = RequestStatus.APPROVED

    def reject(self, request):
        from app.domain.states.rejected_state import RejectedState
        request.state = RejectedState()
        request.status = RequestStatus.REJECTED

    def complete(self, request):
        raise Exception("Cannot complete before approval")
