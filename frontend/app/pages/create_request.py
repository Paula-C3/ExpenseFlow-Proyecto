import streamlit as st

from auth import require_login
from services.api_client import create_request

st.set_page_config(
    page_title="Nueva Solicitud",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""

""", unsafe_allow_html=True)

require_login()

st.title("Nueva Solicitud")

with st.form("create_request_form"):

    title = st.text_input("Título")

    description = st.text_area("Descripción")

    amount = st.number_input(
        "Monto",
        min_value=0.0,
        step=1.0
    )

    currency = st.selectbox(
        "Moneda",
        ["USD", "EUR", "COP"]
    )

    category_label = st.selectbox(
        "Categoría",
        [
            "Transporte",
            "Viaje",
            "Herramientas",
            "Eventos",
            "Capacitación",
            "Relaciones",
            "Otro",
        ],
    )

    category_map = {
        "Transporte": "TRANSPORTATION",
        "Viaje": "TRAVEL",
        "Herramientas": "TOOLS",
        "Eventos": "EVENTS",
        "Capacitación": "TRAINING",
        "Relaciones": "RELATIONSHIPS",
        "Otro": "OTHER",
    }

    receipt_url = st.text_input(
        "URL del comprobante",
        placeholder="Opcional"
    )

    submitted = st.form_submit_button(
        "Crear solicitud",
        use_container_width=True
    )

if submitted:

    if not title.strip():
        st.warning("El título es obligatorio.")
        st.stop()

    if amount <= 0:
        st.warning("El monto debe ser mayor a 0.")
        st.stop()

    payload = {
        "title": title.strip(),
        "description": description.strip() or None,
        "amount": amount,
        "currency": currency,
        "category": category_map[category_label],
        "receipt_url": receipt_url.strip() or None,
    }

    res = create_request(payload)

    if res.status_code in (200, 201):
        st.success("Solicitud creada correctamente.")
    elif res.status_code == 401:
        st.error("Tu sesión expiró. Inicia sesión otra vez.")
    else:
        st.error(f"No se pudo crear la solicitud. Código: {res.status_code}")

        try:
            st.write(res.json())
        except Exception:
            st.write(res.text)

st.markdown("---")

if st.button("Volver al dashboard", use_container_width=True):
    st.switch_page("pages/home.py")