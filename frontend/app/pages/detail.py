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