import importlib
import streamlit as st

from frontend.app.services import api_client


def test_audit_view_renders_in_chronological_order(monkeypatch):
    # Preparar session con rol ADMIN
    monkeypatch.setattr(st, "session_state", {"role": "ADMIN"})

    # Logs desordenados
    logs = [
        {"id": 1, "actor_id": 10, "action": "UPDATE", "previous_state": "A", "new_state": "B", "timestamp": "2026-05-01T10:00:00Z"},
        {"id": 2, "actor_id": 11, "action": "CREATE", "previous_state": None, "new_state": "A", "timestamp": "2026-05-03T12:00:00Z"},
        {"id": 3, "actor_id": 12, "action": "DELETE", "previous_state": "B", "new_state": None, "timestamp": "2026-05-02T09:00:00Z"},
    ]

    def fake_get_audit_logs(request_id=None):
        return logs

    monkeypatch.setattr(api_client, "get_audit_logs", fake_get_audit_logs)

    recorded = {"tables": [], "writes": []}

    def fake_table(rows):
        recorded["tables"].append(rows)

    def fake_write(msg, *a, **kw):
        recorded["writes"].append(str(msg))

    monkeypatch.setattr(st, "table", fake_table)
    monkeypatch.setattr(st, "write", fake_write)

    import frontend.app.pages.audit as audit
    importlib.reload(audit)

    # One table should have been rendered with rows ordered by timestamp desc
    assert recorded["tables"], "No table rendered"
    table_rows = recorded["tables"][0]
    timestamps = [r["timestamp"] for r in table_rows]
    assert timestamps == sorted(timestamps, reverse=True)
