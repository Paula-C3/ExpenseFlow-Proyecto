import requests
import streamlit as st

BASE_URL = "http://backend:8000"

class SessionExpired(Exception):
    pass

def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

def _handle_response(res):
    if res.status_code == 401:
        st.session_state.clear()
        raise SessionExpired("Sesion expirada")
    if res.status_code == 403:
        st.error("Sin permisos para esta accion")
        raise PermissionError("Sin permisos")
    if res.status_code >= 500:
        st.error("Error del servidor")
        raise RuntimeError("Error del servidor")
    return res

# --- Funciones de Pamela ---
def login(email, password):
    # El login no lleva token ni suele mockearse igual
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    _handle_response(res)
    return res.json()

def get_requests(use_mock=False):
    if use_mock:
        return [{"id": 1, "title": "Mock Request", "amount": 100, "status": "SUBMITTED"}]
    res = requests.get(f"{BASE_URL}/requests", headers=_headers())
    return _handle_response(res).json()

def get_request_detail(request_id, use_mock=False):
    if use_mock:
        return {"id": request_id, "title": "Mock Detail", "amount": 100, "status": "SUBMITTED"}
    res = requests.get(f"{BASE_URL}/requests/{request_id}", headers=_headers())
    return _handle_response(res).json()

def create_request(data, use_mock=False):
    if use_mock:
        return {"status": "created", "id": 99}
    res = requests.post(f"{BASE_URL}/requests", json=data, headers=_headers())
    return _handle_response(res).json()

# --- Funciones de Giuliana (Tu parte) ---
def approve_request(request_id, comment=None, use_mock=False):
    if use_mock:
        return {"id": request_id, "status": "APPROVED"}
    payload = {"comment": comment} if comment else {}
    res = requests.post(f"{BASE_URL}/requests/{request_id}/approve", json=payload, headers=_headers())
    return _handle_response(res).json()

def reject_request(request_id, reason, use_mock=False):
    if use_mock:
        return {"id": request_id, "status": "REJECTED"}
    # La razon es obligatoria segun el DTO de la parte de Paula
    res = requests.post(f"{BASE_URL}/requests/{request_id}/reject", json={"reason": reason}, headers=_headers())
    return _handle_response(res).json()

def get_notifications(use_mock=False):
    if use_mock:
        return [{"id": 1, "title": "Aviso", "message": "Mensaje de prueba", "created_at": "2026-05-02"}]
    res = requests.get(f"{BASE_URL}/notifications", headers=_headers())
    return _handle_response(res).json()

def get_audit_logs(request_id=None, use_mock=False):
    if use_mock:
        return [{"actor_id": 1, "action": "LOGIN", "timestamp": "2026-05-02"}]
    url = f"{BASE_URL}/audit"
    if request_id:
        url += f"?request_id={request_id}"
    res = requests.get(url, headers=_headers())
    return _handle_response(res).json()