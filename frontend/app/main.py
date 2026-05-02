import streamlit as st

st.set_page_config(page_title="ExpenseFlow")

if "token" not in st.session_state:
    st.session_state["token"] = None

if st.session_state["token"]:
    st.switch_page("pages/home.py")
else:
    st.switch_page("pages/login.py")