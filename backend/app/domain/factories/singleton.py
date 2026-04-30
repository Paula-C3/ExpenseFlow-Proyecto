from typing import Any, Dict


class SingletonMeta(type):
    """Metaclass para Singleton."""
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=SingletonMeta):
    """Clase Singleton para configuraciones globales."""

    def __init__(self):
        self.database_url: str = ""
        self.secret_key: str = ""
        self.algorithm: str = "HS256"
        self.access_token_expire_minutes: int = 30
        self.debug: bool = False

    def set_database_url(self, url: str) -> None:
        """Establece la URL de la base de datos."""
        self.database_url = url

    def set_secret_key(self, key: str) -> None:
        """Establece la clave secreta para JWT."""
        self.secret_key = key

    def set_debug(self, debug: bool) -> None:
        """Establece el modo debug."""
        self.debug = debug


class EventBusRegistry(metaclass=SingletonMeta):
    """Registro global del Event Bus."""

    def __init__(self):
        self._event_bus: Any = None

    def set_event_bus(self, event_bus: Any) -> None:
        """Registra el event bus."""
        self._event_bus = event_bus

    def get_event_bus(self) -> Any:
        """Obtiene el event bus."""
        if self._event_bus is None:
            raise RuntimeError("Event bus no ha sido registrado")
        return self._event_bus
