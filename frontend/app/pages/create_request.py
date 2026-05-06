import streamlit as st
from services.api_client import create_request

st.title("Crear Solicitud")

title = st.text_input("Título")
amount = st.number_input("Monto")

if st.button("Enviar"):
    if not title or amount <= 0:
        st.warning("Completa todos los campos")
    else:
        res = create_request({
            "title": title,
            "amount": amount
        })

        if res.status_code in [200, 201]:
            st.success("Solicitud creada")
            st.switch_page("app/pages/home.py")
        else:
            st.error("Error al crear solicitud")