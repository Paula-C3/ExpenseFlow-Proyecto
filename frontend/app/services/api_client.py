import os

import requests
import streamlit as st

BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")
TIMEOUT = 10


def _headers() -> dict[str, str]:
    token = st.session_state.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def _request(method: str, path: str, **kwargs):
    return requests.request(
        method=method,
        url=f"{BASE_URL}{path}",
        timeout=TIMEOUT,
        **kwargs,
    )


def login_user(email: str, password: str):
    return _request(
        "POST",
        "/auth/login",
        json={"email": email, "password": password},
    )


def login(email: str, password: str):
    return login_user(email, password)


def get_requests():
    return _request("GET", "/requests", headers=_headers())


def get_request_detail(request_id: int):
    return _request("GET", f"/requests/{request_id}", headers=_headers())


def create_request(data: dict):
    return _request("POST", "/requests", json=data, headers=_headers())

def get_notifications():
    return _request(
        "GET",
        "/notifications",
        headers=_headers(),
    )


def mark_notification_as_read(notification_id: int):
    return _request(
        "PATCH",
        f"/notifications/{notification_id}/read",
        headers=_headers(),
    )