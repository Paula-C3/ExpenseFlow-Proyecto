import pytest

from app.domain.entities.request import Request
from app.domain.states.submitted_state import SubmittedState
from app.domain.states.manager_review_state import ManagerReviewState
from app.domain.states.approved_state import ApprovedState
from app.domain.states.rejected_state import RejectedState
from app.domain.enums import RequestStatus, ExpenseCategory


def make_request(state):
    return Request(
        employee_id=1,
        title="Test expense",
        amount=100.0,
        category=ExpenseCategory.TOOLS,
        state=state,
    )


def test_submitted_approve():
    """SUBMITTED → APPROVED via approve()"""
    request = make_request(SubmittedState())
    assert request.status == RequestStatus.SUBMITTED
    request.approve()
    assert request.status == RequestStatus.APPROVED


def test_submitted_reject():
    """SUBMITTED → REJECTED via reject()"""
    request = make_request(SubmittedState())
    request.reject()
    assert request.status == RequestStatus.REJECTED


def test_submitted_submit_raises():
    """SUBMITTED → submit() lanza excepción"""
    request = make_request(SubmittedState())
    with pytest.raises(Exception):
        request.submit()


def test_manager_review_to_approved():
    """MANAGER_REVIEW → APPROVED"""
    request = make_request(ManagerReviewState())
    request.approve()
    assert request.status == RequestStatus.APPROVED


def test_manager_review_to_rejected():
    """MANAGER_REVIEW → REJECTED"""
    request = make_request(ManagerReviewState())
    request.reject()
    assert request.status == RequestStatus.REJECTED


def test_rejected_can_resubmit():
    """REJECTED → submit() permite reenviar"""
    request = make_request(RejectedState())
    request.submit()
    assert request.status == RequestStatus.SUBMITTED


def test_approved_complete():
    """APPROVED → complete()"""
    request = make_request(ApprovedState())
    request.complete()
