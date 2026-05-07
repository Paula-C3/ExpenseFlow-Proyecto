from abc import ABC, abstractmethod
from app.domain.value_objects import Money


class IApprovalStrategy(ABC):
    @abstractmethod
    def requires_additional_approval(self, request) -> bool:
        pass


class SimpleApprovalStrategy(IApprovalStrategy):
    """Gastos bajos: solo necesitan aprobación del manager."""
    def requires_additional_approval(self, request) -> bool:
        return False


class HighAmountApprovalStrategy(IApprovalStrategy):
    """Gastos >= $1000: necesitan aprobación adicional de Finance."""
    THRESHOLD = 1000.0

    def requires_additional_approval(self, request) -> bool:
        amount = request.amount.amount if hasattr(request.amount, "amount") else float(request.amount)
        return amount >= self.THRESHOLD


class ApprovalStrategySelector:
    """Selecciona la estrategia correcta según el monto del request."""

    @staticmethod
    def select(request) -> IApprovalStrategy:
        amount = request.amount.amount if hasattr(request.amount, "amount") else float(request.amount)
        if amount >= HighAmountApprovalStrategy.THRESHOLD:
            return HighAmountApprovalStrategy()
        return SimpleApprovalStrategy()
