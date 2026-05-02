import importlib
import streamlit as st
import pytest

from frontend.app.services import api_client


def test_employee_role_hides_actions(monkeypatch, tmp_path):
    # Preparar session_state con role EMPLOYEE y request_id
    monkeypatch.setattr(st, "session_state", {"role": "EMPLOYEE", "request_id": 1})

    # Mock del detalle de la solicitud para evitar llamadas reales
    def fake_get_request_detail(request_id):
        return {"id": request_id, "title": "T", "amount": 10, "status": "SUBMITTED"}

    monkeypatch.setattr(api_client, "get_request_detail", fake_get_request_detail)

    # Contador para botones renderizados
    recorded = {"labels": []}

    def fake_button(label, *args, **kwargs):
        recorded["labels"].append(label)
        return False

    monkeypatch.setattr(st, "button", fake_button)

    # Importar (o recargar) el módulo de la página para ejecutar su código
    import frontend.app.pages.detail as detail
    importlib.reload(detail)

    # Verificar que no se haya intentado renderizar botones de aprobación/rechazo
    assert not any("Aprobar" in lbl or "Rechazar" in lbl for lbl in recorded["labels"])
