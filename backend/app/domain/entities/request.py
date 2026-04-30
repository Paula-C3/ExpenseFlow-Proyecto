from app.domain.states.submitted_state import SubmittedState

class Request:

    def __init__(self, id, title, user_id):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.state = SubmittedState()

    def submit(self):
        self.state.submit(self)

    def approve(self):
        self.state.approve(self)

    def reject(self):
        self.state.reject(self)

    def complete(self):
        self.state.complete(self)