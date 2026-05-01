import pytest

from backend.app.domain.entities.request import (
    Request,
    SubmittedState,
    ManagerReviewState,
    ApprovedState,
    RejectedState,
)
from backend.app.domain.enums import RequestStatus
from backend.app.domain.exceptions import InvalidStateTransition


def test_submitted_to_manager_review():
    """Test: SUBMITTED → MANAGER_REVIEW válido."""
    request = Request(state=SubmittedState())
    assert request.status == RequestStatus.SUBMITTED
    
    request.transition_to(RequestStatus.MANAGER_REVIEW)
    assert request.status == RequestStatus.MANAGER_REVIEW


def test_submitted_to_cancelled():
    """Test: SUBMITTED → CANCELLED válido."""
    request = Request(state=SubmittedState())
    request.transition_to(RequestStatus.CANCELLED)
    assert request.status == RequestStatus.CANCELLED


def test_invalid_transition():
    """Test: APPROVED → SUBMITTED lanza excepción."""
    request = Request(state=ApprovedState())
    
    with pytest.raises(InvalidStateTransition):
        request.transition_to(RequestStatus.SUBMITTED)


def test_manager_review_to_approved():
    """Test: MANAGER_REVIEW → APPROVED válido."""
    request = Request(state=ManagerReviewState())
    request.transition_to(RequestStatus.APPROVED)
    assert request.status == RequestStatus.APPROVED


def test_manager_review_to_rejected():
    """Test: MANAGER_REVIEW → REJECTED válido."""
    request = Request(state=ManagerReviewState())
    request.transition_to(RequestStatus.REJECTED)
    assert request.status == RequestStatus.REJECTED


def test_rejected_to_submitted():
    """Test: REJECTED → SUBMITTED válido para reenvio."""
    request = Request(state=RejectedState())
    request.transition_to(RequestStatus.SUBMITTED)
    assert request.status == RequestStatus.SUBMITTED
