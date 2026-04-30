import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """Value Object para Email con validación."""
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError(f"Email inválido: {self.value}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Valida formato de email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Money:
    """Value Object para Dinero con validación."""
    amount: float
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError(f"El monto no puede ser negativo: {self.amount}")

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"


@dataclass(frozen=True)
class RequestTitle:
    """Value Object para Título de solicitud con validación."""
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("El título no puede estar vacío")
        if len(self.value) > 200:
            raise ValueError("El título no puede exceder 200 caracteres")

    def __str__(self) -> str:
        return self.value
