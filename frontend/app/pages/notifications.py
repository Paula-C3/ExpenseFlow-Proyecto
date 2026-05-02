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

st.title("Notificaciones")

try:
    notes = api_client.get_notifications()
except api_client.SessionExpired:
    st.session_state.clear()
    st.experimental_rerun()
except Exception:
    st.error("Error al cargar notificaciones")
    notes = []

if not notes:
    st.write("No tienes notificaciones")
else:
    for n in notes:
        t = n.get("notification_type") or n.get("title") or "Notificación"
        msg = n.get("message", "")
        ts = n.get("created_at")
        unread = not n.get("is_read", False)
        label = f"{t} - {ts}" if ts else t
        if unread:
            st.markdown(f"**{label}**")
        else:
            st.markdown(label)
        st.write(msg)
        st.divider()
