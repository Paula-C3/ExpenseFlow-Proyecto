import streamlit as st

st.set_page_config(
    page_title="ExpenseFlow",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultar navegación automática de páginas
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    st.switch_page("pages/home.py")

st.title("ExpenseFlow")

st.write("Sistema de gestión de gastos corporativos")

col1, col2 = st.columns(2)

with col1:
    if st.button("Iniciar Sesión", use_container_width=True):
        st.switch_page("pages/login.py")

with col2:
    if st.button("Ir al Dashboard", use_container_width=True):
        if st.session_state["authenticated"]:
            st.switch_page("pages/home.py")
        else:
            st.error("Debes iniciar sesión")