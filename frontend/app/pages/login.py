import streamlit as st
import importlib
import os
import importlib.util

def _load_compat():
    try:
        return importlib.import_module("app.pages._compat_imports")
    except Exception:
        try:
            return importlib.import_module("frontend.app.pages._compat_imports")
        except Exception:
            path = os.path.join(os.path.dirname(__file__), "_compat_imports.py")
            spec = importlib.util.spec_from_file_location("compat_imports_local", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod

compat = _load_compat()
api_client = compat.get_api_client()

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
        try:
            st.switch_page("app/pages/home.py")
        except Exception:
            pass