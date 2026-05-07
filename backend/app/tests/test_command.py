from unittest.mock import MagicMock
from backend.app.application.patterns.command import (
    CommandHandler, ApproveRequestCommand, RejectRequestCommand
)
from backend.app.domain.enums import RoleType


def test_handler_dispatches_approve():
    approve_uc = MagicMock()
    reject_uc = MagicMock()
    handler = CommandHandler(approve_use_case=approve_uc, reject_use_case=reject_uc)

    cmd = ApproveRequestCommand(request_id=1, approver_id=5, role=RoleType.MANAGER.value, comment="ok")
    handler.handle(cmd)

    approve_uc.execute.assert_called_once()
    reject_uc.execute.assert_not_called()


def test_handler_dispatches_reject():
    approve_uc = MagicMock()
    reject_uc = MagicMock()
    handler = CommandHandler(approve_use_case=approve_uc, reject_use_case=reject_uc)

    cmd = RejectRequestCommand(request_id=1, rejector_id=5, role=RoleType.MANAGER.value, reason="no aplica")
    handler.handle(cmd)

    reject_uc.execute.assert_called_once()
    approve_uc.execute.assert_not_called()


def test_unknown_command_raises():
    import pytest
    from backend.app.application.patterns.command import Command

    handler = CommandHandler(approve_use_case=MagicMock(), reject_use_case=MagicMock())
    with pytest.raises(ValueError):
        handler.handle(Command())
