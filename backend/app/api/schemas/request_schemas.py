from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.domain.enums import RequestStatus, ExpenseCategory


class CreateRequestDTO(BaseModel):
    """DTO para crear solicitud."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    amount: float = Field(..., gt=0)
    category: ExpenseCategory
    receipt_url: Optional[str] = None


class RequestResponseDTO(BaseModel):
    """DTO para respuesta de solicitud."""
    id: int
    employee_id: int
    title: str
    description: Optional[str]
    amount: float
    currency: str
    category: ExpenseCategory
    receipt_url: Optional[str]
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
    manager_id: Optional[int] = None
    finance_id: Optional[int] = None

    class Config:
        from_attributes = True


class ApproveRequestDTO(BaseModel):
    """DTO para aprobar solicitud."""
    comment: Optional[str] = Field(None, max_length=500)


class RejectRequestDTO(BaseModel):
    """DTO para rechazar solicitud."""
    reason: str = Field(..., min_length=1, max_length=500)
