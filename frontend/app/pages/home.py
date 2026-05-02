import streamlit as st
import importlib
import os
import importlib.util

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

# Indicador de notificaciones en sidebar
try:
    _notes = api_client.get_notifications()
    unread = sum(1 for n in _notes if not n.get("is_read", False))
    st.sidebar.write(f"Notificaciones ({unread})")
except Exception:
    # No bloquear la página por errores en notificaciones
    pass

st.title("Solicitudes")

try:
    requests_list = api_client.get_requests()
except api_client.SessionExpired:
    st.session_state.clear()
    st.experimental_rerun()
except Exception:
    st.error("Error al cargar solicitudes")
else:
    for r in requests_list:
        if st.button(f"{r['id']} - {r['title']} ({r['status']})"):
            st.session_state["request_id"] = r["id"]
            try:
                st.switch_page("app/pages/detail.py")
            except Exception:
                pass

if st.button("Crear solicitud"):
    try:
        st.switch_page("app/pages/create_request.py")
    except Exception:
        pass