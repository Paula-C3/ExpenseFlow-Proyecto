import streamlit as st

from auth import require_login
from services.api_client import (
    get_notifications,
    mark_notification_as_read
)

st.set_page_config(
    page_title="Notificaciones",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""

""", unsafe_allow_html=True)

require_login()

st.title("Historial de Notificaciones")

res = get_notifications()

if res.status_code != 200:
    st.error("No se pudieron cargar las notificaciones.")
    st.stop()

notifications = res.json()

if not notifications:
    st.info("No tienes notificaciones.")
    st.stop()

for n in notifications:

    with st.container(border=True):

        col1, col2 = st.columns([8, 2])

        with col1:
            st.subheader(n["title"])

            st.write(n["message"])

            st.caption(
                f"""
                Tipo: {n['notification_type']} |
                Fecha: {n['created_at']}
                """
            )

            if n["is_read"]:
                st.success("Leída")
            else:
                st.warning("No leída")

        with col2:

            if not n["is_read"]:

                if st.button(
                    "Marcar leída",
                    key=f"read_{n['id']}"
                ):

                    response = mark_notification_as_read(
                        n["id"]
                    )

                    if response.status_code == 200:
                        st.rerun()