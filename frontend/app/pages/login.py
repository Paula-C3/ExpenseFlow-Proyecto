import streamlit as st
from frontend.app.services import api_client

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        data = api_client.login(email, password)
    except Exception:
        st.error("Credenciales incorrectas")
    else:
        st.session_state["token"] = data.get("access_token")
        st.session_state["role"] = data.get("role")
        st.switch_page("app/pages/home.py")