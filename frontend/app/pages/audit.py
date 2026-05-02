import streamlit as st
try:
    from app.pages._compat_imports import get_api_client
except Exception:
    try:
        from frontend.app.pages._compat_imports import get_api_client
    except Exception:
        import importlib.util, os
        path = os.path.join(os.path.dirname(__file__), "_compat_imports.py")
        spec = importlib.util.spec_from_file_location("_compat_imports_local", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        get_api_client = module.get_api_client

api_client = get_api_client()

st.title("Auditoría")

role = st.session_state.get("role")
if role != "ADMIN":
    st.error("Acceso denegado: se requiere rol ADMIN")
else:
    try:
        logs = api_client.get_audit_logs()
    except api_client.SessionExpired:
        st.session_state.clear()
        st.experimental_rerun()
    except Exception:
        st.error("Error al cargar logs de auditoría")
        logs = []

    # Ordenar: más reciente primero
    def _ts_key(l):
        return l.get("timestamp") or l.get("created_at")

    sorted_logs = sorted(logs, key=_ts_key, reverse=True)

    if not sorted_logs:
        st.write("No hay registros de auditoría")
    else:
        # Mostrar tabla simple
        rows = []
        for log in sorted_logs:
            rows.append({
                "actor_id": log.get("actor_id"),
                "action": log.get("action"),
                "entity": f"{log.get('entity_type')}#{log.get('entity_id')}",
                "from": log.get("previous_state"),
                "to": log.get("new_state"),
                "timestamp": log.get("timestamp") or log.get("created_at"),
            })
        st.table(rows)
        import importlib
        import os

        def _load_compat():
            try:
                return importlib.import_module("app.pages._compat_imports")
            except Exception:
                try:
                    return importlib.import_module("frontend.app.pages._compat_imports")
                except Exception:
                    path = os.path.join(os.path.dirname(__file__), "_compat_imports.py")
                    spec = importlib.util.spec_from_file_location("compat_imports_local", path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    return mod

        compat = _load_compat()
        api_client = compat.get_api_client()
