import streamlit as st          #type: ignore
from services.api_client import login

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    res = login(email, password)

    if res.status_code == 200:
        data = res.json()
        st.session_state["token"] = data["access_token"]
        st.session_state["role"] = data["role"]
        st.switch_page("pages/home.py") #type: ignore
    else:
        st.error("Credenciales incorrectas")