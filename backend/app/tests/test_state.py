import pytest
from backend.app.domain.states.submitted_state import SubmittedState
from backend.app.domain.states.approved_state import ApprovedState
from backend.app.domain.states.rejected_state import RejectedState
from backend.app.domain.states.completed_state import CompletedState
from backend.app.domain.entities.request import Request
from backend.app.domain.enums import RequestStatus, ExpenseCategory
from backend.app.domain.value_objects import Money, RequestTitle
from datetime import datetime


def make_request(state=None):
    return Request(
        employee_id=1,
        title=RequestTitle("Test"),
        amount=Money(100.0, "USD"),
        category=ExpenseCategory.OTHER,
        status=RequestStatus.SUBMITTED,
        state=state,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        submitted_by_id=1,
    )


def test_submitted_to_approved():
    request = make_request(SubmittedState())
    request.approve()
    assert request.status == RequestStatus.APPROVED
    assert isinstance(request.state, ApprovedState)


def test_submitted_to_rejected():
    request = make_request(SubmittedState())
    request.reject()
    assert request.status == RequestStatus.REJECTED
    assert isinstance(request.state, RejectedState)


def test_approved_to_completed():
    request = make_request(ApprovedState())
    request.status = RequestStatus.APPROVED
    request.complete()
    assert isinstance(request.state, CompletedState)


def test_approved_cannot_be_submitted_again():
    request = make_request(ApprovedState())
    with pytest.raises(Exception, match="Already submitted"):
        request.submit()


def test_approved_cannot_be_rejected():
    request = make_request(ApprovedState())
    with pytest.raises(Exception, match="Cannot reject after approval"):
        request.reject()


def test_rejected_can_resubmit():
    request = make_request(RejectedState())
    request.submit()
    assert request.status == RequestStatus.SUBMITTED
    assert isinstance(request.state, SubmittedState)


def test_completed_blocks_all():
    request = make_request(CompletedState())
    with pytest.raises(Exception):
        request.submit()
    with pytest.raises(Exception):
        request.approve()
    with pytest.raises(Exception):
        request.reject()
    with pytest.raises(Exception):
        request.complete()