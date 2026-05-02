import streamlit as st

st.set_page_config(page_title="ExpenseFlow")

if "token" not in st.session_state:
    st.session_state["token"] = None
def _exec_page(module_names):
    """Try to import one of module names to execute its top-level Streamlit UI."""
    import importlib
    for name in module_names:
        try:
            importlib.import_module(name)
            return True
        except Exception:
            continue
    return False


if st.session_state["token"]:
    try:
        st.switch_page("pages/home.py")
    except Exception:
        # fallback: try importing the home page module so its UI runs
        _exec_page(["app.pages.home", "frontend.app.pages.home", "frontend.app.pages.home"])
else:
    try:
        st.switch_page("pages/login.py")
    except Exception:
        # fallback: import/execute login page top-level UI
        _exec_page(["app.pages.login", "frontend.app.pages.login", "frontend.app.pages.login"])