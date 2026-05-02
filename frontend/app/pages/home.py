import streamlit as st
from frontend.app.services import api_client

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
            st.switch_page("app/pages/detail.py")

if st.button("Crear solicitud"):
    st.switch_page("app/pages/create_request.py")