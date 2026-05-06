class Approval:
    def __init__(self, id, request_id, approver_id, status):
        self.id = id
        self.request_id = request_id
        self.approver_id = approver_id
        self.status = status