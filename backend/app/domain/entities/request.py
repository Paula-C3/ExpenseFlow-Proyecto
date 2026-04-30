from app.domain.states.submitted_state import SubmittedState

class Request:

    def __init__(self, id, title, user_id, event_bus=None, approver_id=None):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.approver_id = approver_id
        self.state = SubmittedState()
        self.event_bus = event_bus

    def submit(self):
        self.state.submit(self)

    def approve(self):
        self.state.approve(self)
        
        if self.event_bus:
            from app.domain.events import RequestApprovedEvent
            self.event_bus.publish(RequestApprovedEvent(
                request_id=self.id,
                approver_id=self.approver_id or self.user_id
            ))

    def reject(self):
        self.state.reject(self)
        
        if self.event_bus:
            from app.domain.events import RequestRejectedEvent
            self.event_bus.publish(RequestRejectedEvent(
                request_id=self.id,
                rejector_id=self.approver_id or self.user_id
            ))

    def complete(self):
        self.state.complete(self)