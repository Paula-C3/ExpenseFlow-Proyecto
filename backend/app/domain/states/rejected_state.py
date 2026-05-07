from app.domain.states.request_state import RequestState
from app.domain.enums import RequestStatus


class RejectedState(RequestState):

    def submit(self, request):
        from app.domain.states.submitted_state import SubmittedState
        request.state = SubmittedState()
        request.status = RequestStatus.SUBMITTED

    def approve(self, request):
        raise Exception("Cannot approve rejected request")

    def reject(self, request):
        raise Exception("Already rejected")

    def complete(self, request):
        raise Exception("Cannot complete rejected request")

