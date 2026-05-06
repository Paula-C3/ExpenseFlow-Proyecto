import streamlit as st
from auth import require_auth, logout

require_auth()

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Dashboard")

st.success("Bienvenido al sistema ExpenseFlow")

col1, col2 = st.columns(2)

with col1:
    if st.button("Crear Solicitud", use_container_width=True):
        st.switch_page("pages/create_request.py")

with col2:
    if st.button("Cerrar Sesión", use_container_width=True):
        logout()
        st.switch_page("main.py")