from unittest.mock import MagicMock
from app.application.patterns.strategy import (
    ApprovalStrategySelector, HighAmountApprovalStrategy, SimpleApprovalStrategy
)
from app.domain.value_objects import Money


def make_request(amount: float):
    r = MagicMock()
    r.amount = Money(amount, "USD")
    return r


def test_low_amount_simple_strategy():
    r = make_request(200.0)
    strategy = ApprovalStrategySelector.select(r)
    assert isinstance(strategy, SimpleApprovalStrategy)
    assert strategy.requires_additional_approval(r) is False


def test_exact_threshold_high_strategy():
    r = make_request(1000.0)
    strategy = ApprovalStrategySelector.select(r)
    assert isinstance(strategy, HighAmountApprovalStrategy)
    assert strategy.requires_additional_approval(r) is True


def test_high_amount_high_strategy():
    r = make_request(5000.0)
    strategy = ApprovalStrategySelector.select(r)
    assert isinstance(strategy, HighAmountApprovalStrategy)
    assert strategy.requires_additional_approval(r) is True
