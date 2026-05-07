import requests
import streamlit as st

from services.api_client import login_user

st.set_page_config(
    page_title="Login",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 520px;
        padding-top: 5rem;
    }
</style>
""", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state["token"] = None

if st.session_state.get("token"):
    st.switch_page("pages/home.py")

st.markdown("""
<div style="text-align:center; margin-bottom: 2rem;">
    <h1 style="font-size: 3rem; margin-bottom: 0.2rem;">ExpenseFlow</h1>
    <p style="font-size: 1.1rem; color: #666;">
        Sistema de gestión de gastos corporativos
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("login_form"):
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    submitted = st.form_submit_button("Iniciar sesión", use_container_width=True)

if submitted:
    if not email.strip() or not password.strip():
        st.warning("Ingresa correo y contraseña.")
        st.stop()

    try:
        res = login_user(email=email.strip(), password=password.strip())
    except requests.RequestException:
        st.error("No se pudo conectar con el backend.")
        st.stop()

    if res.status_code == 200:
        data = res.json()

        st.session_state["token"] = data.get("access_token")
        st.session_state["role"] = data.get("role")
        st.session_state["user_id"] = data.get("user_id")

        st.success("Inicio de sesión correcto.")
        st.switch_page("pages/home.py")
    else:
        st.error("Correo o contraseña incorrectos.")