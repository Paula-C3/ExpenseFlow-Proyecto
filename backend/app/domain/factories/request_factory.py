from datetime import datetime
from typing import Dict, Any

from app.domain.entities.request import Request
from app.domain.states.submitted_state import SubmittedState
from app.domain.enums import ExpenseCategory, RequestStatus
from app.domain.value_objects import Money, RequestTitle


class RequestFactory:
    """Factory para crear solicitudes de gasto."""

    @staticmethod
    def create(
        employee_id: int,
        title: str,
        amount: float,
        category: ExpenseCategory = ExpenseCategory.OTHER,
        description: str = "",
        receipt_url: str = None,
    ) -> Request:
        """
        Crea una nueva solicitud en estado SUBMITTED.
        
        Args:
            employee_id: ID del empleado que crea la solicitud
            title: Título de la solicitud
            amount: Monto en USD
            category: Categoría del gasto
            description: Descripción detallada
            receipt_url: URL del comprobante (opcional)
            
        Returns:
            Instancia de Request con estado inicial SUBMITTED
        """
        request = Request(
            employee_id=employee_id,
            title=RequestTitle(title),
            amount=Money(amount, "USD"),
            category=category,
            description=description,
            receipt_url=receipt_url,
            state=SubmittedState(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            submitted_by_id=employee_id,
        )
        return request

    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> Request:
        """
        Crea una solicitud desde un diccionario.
        
        Args:
            data: Diccionario con los datos de la solicitud
            
        Returns:
            Instancia de Request
        """
        return RequestFactory.create(
            employee_id=data.get("employee_id"),
            title=data.get("title"),
            amount=data.get("amount"),
            category=ExpenseCategory(data.get("category", "OTHER")),
            description=data.get("description", ""),
            receipt_url=data.get("receipt_url"),
        )
