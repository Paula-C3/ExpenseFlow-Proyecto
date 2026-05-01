from backend.app.domain.states.request_state import RequestState


class ApprovedState(RequestState):

    def submit(self, request):
        raise Exception("Already submitted")

    def approve(self, request):
        raise Exception("Already approved")

    def reject(self, request):
        raise Exception("Cannot reject after approval")

    def complete(self, request):
        from backend.app.domain.states.completed_state import CompletedState
        from backend.app.domain.enums import RequestStatus
        request.state = CompletedState()
        request.status = RequestStatus.PAID
