import streamlit as st
from frontend.app.services import api_client

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
