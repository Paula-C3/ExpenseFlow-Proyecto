"""Excepciones del dominio."""


class DomainException(Exception):
    """Excepción base del dominio."""
    pass


class InvalidStateTransition(DomainException):
    """Se intenta hacer una transición de estado inválida."""
    pass


class UnauthorizedAction(DomainException):
    """Acción no autorizada por el usuario."""
    pass


class PermissionDenied(DomainException):
    """Usuario no tiene permisos para esta acción."""
    pass


class ResourceNotFound(DomainException):
    """Recurso no encontrado."""
    pass


class InvalidEmail(DomainException):
    """Email inválido."""
    pass


class InvalidAmount(DomainException):
    """Monto inválido."""
    pass
