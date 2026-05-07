from abc import ABC, abstractmethod


class RequestProcessor(ABC):
    """Template Method: define el esqueleto del flujo de procesamiento."""

    def process(self, request, actor_id: int, role: str):
        self.validate(request, actor_id, role)
        self.execute(request, actor_id)
        self.notify(request)
        self.audit(request, actor_id)

    @abstractmethod
    def validate(self, request, actor_id: int, role: str):
        pass

    @abstractmethod
    def execute(self, request, actor_id: int):
        pass

    def notify(self, request):
        """Hook opcional — subclase puede sobreescribir."""
        pass

    def audit(self, request, actor_id: int):
        """Hook opcional — subclase puede sobreescribir."""
        pass


class ApproveRequestProcessor(RequestProcessor):
    """Procesador concreto para aprobación de solicitudes."""

    def __init__(self, repo, event_bus):
        self.repo = repo
        self.event_bus = event_bus
        self.steps_called = []  # usado en tests para verificar orden

    def validate(self, request, actor_id: int, role: str):
        from app.domain.enums import RoleType
        allowed = {RoleType.MANAGER.value, RoleType.FINANCE_ADMIN.value, RoleType.SYSTEM_ADMIN.value}
        if role not in allowed:
            raise PermissionError("Rol no autorizado para aprobar")
        self.steps_called.append("validate")

    def execute(self, request, actor_id: int):
        request.event_bus = self.event_bus
        request.approve(approver_id=actor_id)
        self.repo.update(request)
        self.steps_called.append("execute")

    def notify(self, request):
        self.steps_called.append("notify")

    def audit(self, request, actor_id: int):
        self.steps_called.append("audit")

