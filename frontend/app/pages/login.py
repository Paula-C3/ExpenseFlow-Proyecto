import streamlit as st
from services.api_client import login_user

st.set_page_config(page_title="Login", layout="centered")

# ocultar sidebar automático
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("Login")

email = st.text_input("Correo")
password = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):

    response = login_user(email, password)

    if response and "access_token" in response:

        st.session_state["authenticated"] = True
        st.session_state["token"] = response["access_token"]
        st.session_state["user"] = response.get("user")

        st.success("Login exitoso")
        st.switch_page("pages/home.py")

    else:
        st.error("Credenciales inválidas")