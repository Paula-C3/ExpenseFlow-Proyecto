import streamlit as st
from frontend.app.services import api_client

st.title("Crear Solicitud")

title = st.text_input("Título")
amount = st.number_input("Monto")

if st.button("Enviar"):
    if not title or amount <= 0:
        st.warning("Completa todos los campos")
    else:
        try:
            data = api_client.create_request({"title": title, "amount": amount})
        except api_client.SessionExpired:
            st.session_state.clear()
            st.experimental_rerun()
        except Exception:
            st.error("Error al crear solicitud")
        else:
            st.success("Solicitud creada")
            st.switch_page("app/pages/home.py")