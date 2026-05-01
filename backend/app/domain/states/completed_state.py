from app.domain.states.request_state import RequestState

class CompletedState(RequestState):

    def submit(self, request):
        raise Exception("Already completed")

    def approve(self, request):
        raise Exception("Already completed")

    def reject(self, request):
        raise Exception("Already completed")

    def complete(self, request):
        raise Exception("Already completed")