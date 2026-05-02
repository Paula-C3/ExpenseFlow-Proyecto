import streamlit as st
from frontend.app.services import api_client

request_id = st.session_state.get("request_id")

st.title("Detalle")

if not request_id:
    st.error("No hay ID")
else:
    try:
        r = api_client.get_request_detail(request_id)
    except api_client.SessionExpired:
        st.session_state.clear()
        st.experimental_rerun()
    except Exception:
        st.error("Error al cargar detalle")
    else:
        st.write(f"ID: {r['id']}")
        st.write(f"Título: {r['title']}")
        st.write(f"Estado: {r['status']}")
        st.write(f"Monto: {r['amount']}")

        # Acciones según rol: solo mostrar botones si el usuario puede aprobar/rechazar
        role = st.session_state.get("role")
        if role in ("APPROVER", "ADMIN"):
            # Aprobar
            if st.button("Aprobar"):
                with st.expander("Confirmar aprobación"):
                    if st.button("Confirmar Aprobar"):
                        try:
                            api_client.approve_request(request_id)
                        except api_client.SessionExpired:
                            st.session_state.clear()
                            st.experimental_rerun()
                        except Exception:
                            st.error("Error al aprobar la solicitud")
                        else:
                            st.success("Solicitud aprobada")
                            st.experimental_rerun()

            # Rechazar
            if st.button("Rechazar"):
                with st.expander("Rechazar solicitud"):
                    reason = st.text_area("Razón del rechazo", key="reject_reason")
                    if st.button("Confirmar Rechazo"):
                        if not reason or not reason.strip():
                            st.error("Debe indicar la razón del rechazo")
                        else:
                            try:
                                api_client.reject_request(request_id, reason)
                            except api_client.SessionExpired:
                                st.session_state.clear()
                                st.experimental_rerun()
                            except Exception:
                                st.error("Error al rechazar la solicitud")
                            else:
                                st.success("Solicitud rechazadda")
                                st.experimental_rerun()

if st.button("Volver"):
    st.switch_page("app/pages/home.py")

# Historial de acciones (cronológico, más reciente primero)
if request_id:
    st.header("Historial de acciones")
    try:
        logs = api_client.get_audit_logs(request_id=request_id)
    except api_client.SessionExpired:
        st.session_state.clear()
        st.experimental_rerun()
    except PermissionError:
        st.error("No tiene permiso para ver el historial")
    except Exception:
        st.error("Error al cargar historial")
    else:
        # Asegurar orden cronológico: del más reciente al más antiguo
        def _ts_key(l):
            return l.get("timestamp") or l.get("created_at")

        sorted_logs = sorted(logs, key=_ts_key, reverse=True)
        if not sorted_logs:
            st.write("No hay historial disponible")
        else:
            for log in sorted_logs:
                actor = log.get("actor_id")
                action = log.get("action")
                prev = log.get("previous_state")
                new = log.get("new_state")
                ts = log.get("timestamp") or log.get("created_at")
                st.write(f"{ts} — Actor: {actor} — {action} — {prev} → {new}")