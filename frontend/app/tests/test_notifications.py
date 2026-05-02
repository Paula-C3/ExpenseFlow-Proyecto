import importlib
import streamlit as st

from frontend.app.services import api_client


def test_notifications_empty(monkeypatch):
    # Mock session and api
    monkeypatch.setattr(st, "session_state", {"token": "t"})

    def fake_get_notifications():
        return []

    monkeypatch.setattr(api_client, "get_notifications", fake_get_notifications)

    recorded = {"writes": []}

    def fake_write(msg, *a, **kw):
        recorded["writes"].append(str(msg))

    monkeypatch.setattr(st, "write", fake_write)

    import frontend.app.pages.notifications as notifications
    importlib.reload(notifications)

    assert any("No tienes notificaciones" in w for w in recorded["writes"]) 


def test_notifications_two_items(monkeypatch):
    monkeypatch.setattr(st, "session_state", {"token": "t"})

    def fake_get_notifications():
        return [
            {"id": 1, "notification_type": "Tipo A", "message": "M1", "created_at": "2026-05-02", "is_read": False},
            {"id": 2, "notification_type": "Tipo B", "message": "M2", "created_at": "2026-05-02", "is_read": True},
        ]

    monkeypatch.setattr(api_client, "get_notifications", fake_get_notifications)

    recorded = {"writes": [], "markdown": []}

    def fake_write(msg, *a, **kw):
        recorded["writes"].append(str(msg))

    def fake_markdown(msg, *a, **kw):
        recorded["markdown"].append(str(msg))

    monkeypatch.setattr(st, "write", fake_write)
    monkeypatch.setattr(st, "markdown", fake_markdown)

    import frontend.app.pages.notifications as notifications
    importlib.reload(notifications)

    # Expect both messages shown
    assert any("M1" in w for w in recorded["writes"]) and any("M2" in w for w in recorded["writes"])
    # One of the markdown entries should contain Tipo A or the timestamp
    assert len(recorded["markdown"]) >= 1
