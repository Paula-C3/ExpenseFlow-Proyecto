import streamlit as st


def is_authenticated():
    return st.session_state.get("authenticated", False)


def require_auth():
    if not is_authenticated():
        st.warning("Debes iniciar sesión")
        st.switch_page("main.py")


def logout():
    st.session_state["authenticated"] = False
    st.session_state["token"] = None
    st.session_state["user"] = None