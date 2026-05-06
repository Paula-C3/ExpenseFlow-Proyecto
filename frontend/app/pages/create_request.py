import streamlit as st
from auth import require_auth
from services.api_client import create_request

require_auth()

st.set_page_config(page_title="Nueva Solicitud", layout="centered")

st.title("Nueva Solicitud")

title = st.text_input("Título")
description = st.text_area("Descripción")
amount = st.number_input("Monto", min_value=0.0)

category = st.selectbox(
    "Categoría",
    [
        "Transporte",
        "Alimentación",
        "Hospedaje",
        "Oficina",
        "Otros"
    ]
)

if st.button("Crear Solicitud"):

    payload = {
        "title": title,
        "description": description,
        "amount": amount,
        "category": category
    }

    response = create_request(
        payload,
        st.session_state["token"]
    )

    if response:
        st.success("Solicitud creada correctamente")
    else:
        st.error("Error al crear solicitud")