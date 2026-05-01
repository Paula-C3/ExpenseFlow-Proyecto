from dataclasses import dataclass
from typing import Optional


@dataclass
class Command:
    pass


@dataclass
class ApproveRequestCommand(Command):
    request_id: int
    approver_id: int
    role: str
    comment: Optional[str] = None


@dataclass
class RejectRequestCommand(Command):
    request_id: int
    rejector_id: int
    role: str
    reason: str


class CommandHandler:
    def __init__(self, approve_use_case, reject_use_case):
        self.approve_use_case = approve_use_case
        self.reject_use_case = reject_use_case

    def handle(self, command: Command):
        from backend.app.application.dtos.request_dto import ApproveRequestDTO, RejectRequestDTO

        if isinstance(command, ApproveRequestCommand):
            dto = ApproveRequestDTO(comment=command.comment)
            return self.approve_use_case.execute(
                request_id=command.request_id,
                dto=dto,
                approver_id=command.approver_id,
                role=command.role,
            )
        elif isinstance(command, RejectRequestCommand):
            dto = RejectRequestDTO(reason=command.reason)
            return self.reject_use_case.execute(
                request_id=command.request_id,
                dto=dto,
                rejector_id=command.rejector_id,
                role=command.role,
            )
        else:
            raise ValueError(f"Command no reconocido: {type(command)}")
