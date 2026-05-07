import streamlit as st

from auth import require_login
from services.api_client import (
    approve_request,
    get_notifications,
    get_request_detail,
    mark_notification_as_read,
    reject_request,
)

st.set_page_config(
    page_title="Notificaciones",
    layout="wide",
    initial_sidebar_state="collapsed",
)

require_login()

st.title("Historial de Notificaciones")


def go_to_detail(request_id: int):
    st.session_state["request_id"] = request_id
    st.switch_page("pages/detail.py")


def can_approve(role: str, status: str) -> bool:
    if role == "MANAGER":
        return status == "MANAGER_REVIEW"
    if role in ("FINANCE_ANALYST", "FINANCE_ADMIN"):
        return status in ("FINANCE_REVIEW", "APPROVED", "READY_FOR_PAYMENT")
    if role == "SYSTEM_ADMIN":
        return status not in ("REJECTED", "CANCELLED", "PAID")
    return False


def can_reject(role: str, status: str) -> bool:
    if role == "MANAGER":
        return status == "MANAGER_REVIEW"
    if role in ("FINANCE_ANALYST", "FINANCE_ADMIN"):
        return status in ("FINANCE_REVIEW", "APPROVED", "READY_FOR_PAYMENT")
    if role == "SYSTEM_ADMIN":
        return status not in ("REJECTED", "CANCELLED", "PAID")
    return False


res = get_notifications()

if res.status_code != 200:
    st.error("No se pudieron cargar las notificaciones.")
    st.stop()

notifications = res.json()
role = st.session_state.get("role")

if not notifications:
    st.info("No tienes notificaciones.")
    st.stop()

for n in notifications:
    request_id = n.get("reference_id")
    request_data = None

    if request_id:
        detail_res = get_request_detail(request_id)
        if detail_res.status_code == 200:
            request_data = detail_res.json()

    with st.container(border=True):
        col1, col2 = st.columns([7, 3])

        with col1:
            st.subheader(n["title"])
            st.write(n["message"])
            st.caption(
                f"Tipo: {n['notification_type']} | Fecha: {n['created_at']}"
            )

            if request_data:
                st.write(
                    f"Solicitud #{request_data['id']} · "
                    f"{request_data['title']} · "
                    f"{request_data['amount']} {request_data['currency']} · "
                    f"Estado: {request_data['status']}"
                )

            if n["is_read"]:
                st.success("Leída")
            else:
                st.warning("No leída")

        with col2:
            if request_id:
                if st.button("Ver detalle", key=f"detail_{n['id']}", use_container_width=True):
                    go_to_detail(request_id)

            if request_data and can_approve(role, request_data["status"]):
                if st.button("Aprobar", key=f"approve_{n['id']}", use_container_width=True):
                    approve_res = approve_request(
                        request_data["id"],
                        "Aprobado desde notificaciones",
                    )
                    if approve_res.status_code == 200:
                        mark_notification_as_read(n["id"])
                        st.success("Solicitud aprobada.")
                        st.rerun()
                    else:
                        st.error(approve_res.json().get("detail", "No se pudo aprobar."))

            if request_data and can_reject(role, request_data["status"]):
                reason = st.text_input("Motivo de rechazo", key=f"reason_{n['id']}")
                if st.button("Rechazar", key=f"reject_{n['id']}", use_container_width=True):
                    if not reason.strip():
                        st.warning("Escribe un motivo para rechazar.")
                    else:
                        reject_res = reject_request(request_data["id"], reason.strip())
                        if reject_res.status_code == 200:
                            mark_notification_as_read(n["id"])
                            st.success("Solicitud rechazada.")
                            st.rerun()
                        else:
                            st.error(reject_res.json().get("detail", "No se pudo rechazar."))

            if not n["is_read"]:
                if st.button("Marcar leída", key=f"read_{n['id']}", use_container_width=True):
                    response = mark_notification_as_read(n["id"])
                    if response.status_code == 200:
                        st.rerun()

st.markdown("---")
if st.button("Volver al dashboard", use_container_width=True):
    st.switch_page("pages/home.py")