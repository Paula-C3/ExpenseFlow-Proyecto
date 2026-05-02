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
            try:
                st.switch_page("app/pages/home.py")
            except Exception:
                pass