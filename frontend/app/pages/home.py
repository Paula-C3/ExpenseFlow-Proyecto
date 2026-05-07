import streamlit as st                  #type: ignore
from services.api_client import get_requests

st.title("Solicitudes")

res = get_requests()

if res.status_code == 200:
    requests = res.json()

    for r in requests:
        if st.button(f"{r['id']} - {r['title']} ({r['status']})"):
            st.session_state["request_id"] = r["id"]
            st.switch_page("pages/detail.py")   #type: ignore
else:
    st.error("Error al cargar solicitudes")

if st.button("Crear solicitud"):
    st.switch_page("pages/create_request.py")   #type: ignore