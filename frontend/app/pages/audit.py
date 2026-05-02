import streamlit as st
from frontend.app.services import api_client

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
