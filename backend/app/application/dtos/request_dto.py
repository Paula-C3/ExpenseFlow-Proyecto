from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from backend.app.domain.enums import RequestStatus, ExpenseCategory


class CreateRequestDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    amount: float = Field(..., gt=0)
    category: ExpenseCategory
    receipt_url: Optional[str] = None


class RequestResponseDTO(BaseModel):
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

    @classmethod
    def from_domain(cls, request) -> "RequestResponseDTO":
        return cls(
            id=request.id,
            employee_id=request.employee_id,
            title=str(request.title),
            description=request.description,
            amount=request.amount.amount if hasattr(request.amount, "amount") else float(request.amount),
            currency=request.amount.currency if hasattr(request.amount, "currency") else "USD",
            category=request.category,
            receipt_url=request.receipt_url,
            status=request.status,
            created_at=request.created_at,
            updated_at=request.updated_at,
            manager_id=request.manager_id,
            finance_id=request.finance_id,
        )


class ApproveRequestDTO(BaseModel):
    comment: Optional[str] = Field(None, max_length=500)


class RejectRequestDTO(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500)
