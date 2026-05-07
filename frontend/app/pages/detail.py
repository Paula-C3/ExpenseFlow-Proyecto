import streamlit as st          #type: ignore
from services.api_client import get_request_detail

request_id = st.session_state.get("request_id")

st.title("Detalle")

if not request_id:
    st.error("No hay ID")
else:
    res = get_request_detail(request_id)

    if res.status_code == 200:
        r = res.json()

        st.write(f"ID: {r['id']}")
        st.write(f"Título: {r['title']}")
        st.write(f"Estado: {r['status']}")
        st.write(f"Monto: {r['amount']}")
    else:
        st.error("Error al cargar detalle")

if st.button("Volver"):
    st.switch_page("pages/home.py") #type: ignore