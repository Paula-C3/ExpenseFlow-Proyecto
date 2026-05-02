import os
import importlib.util


def get_api_client():
    """Intentar importar `api_client` con varios fallbacks.

    Orden de intentos:
    1. `app.services.api_client`
    2. `frontend.app.services.api_client`
    3. Cargar desde el archivo `../services/api_client.py` relativo a este directorio
    """
    try:
        from app.services import api_client
        return api_client
    except Exception:
        try:
            from frontend.app.services import api_client
            return api_client
        except Exception:
            base_dir = os.path.dirname(__file__)  # pages dir
            path = os.path.normpath(os.path.join(base_dir, "..", "services", "api_client.py"))
            if not os.path.exists(path):
                raise ImportError(f"Could not locate api_client at {path}")
            spec = importlib.util.spec_from_file_location("api_client_local", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
