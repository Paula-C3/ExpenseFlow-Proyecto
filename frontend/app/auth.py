import streamlit as st


def is_authenticated():
    return st.session_state.get("token") is not None


def require_login():
    if not is_authenticated():
        st.warning("Debes iniciar sesión")
        st.switch_page("pages/login.py")


def logout():
    st.session_state["token"] = None
    st.session_state["role"] = None
    st.session_state["user_id"] = None