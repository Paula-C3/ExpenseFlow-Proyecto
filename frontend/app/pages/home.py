import streamlit as st

from auth import require_login, logout

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

require_login()

st.title("Dashboard")

st.success("Bienvenido a ExpenseFlow")

st.write(f"Rol actual: {st.session_state.get('role')}")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Crear Solicitud", use_container_width=True):
        st.switch_page("pages/create_request.py")

with col2:
    if st.button("Notificaciones", use_container_width=True):
        st.switch_page("pages/notifications.py")

with col3:
    if st.button("Cerrar Sesión", use_container_width=True):
        logout()
        st.switch_page("pages/login.py")