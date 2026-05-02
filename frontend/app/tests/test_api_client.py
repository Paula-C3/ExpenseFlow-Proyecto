import pytest
from requests.models import Response

from frontend.app.services import api_client


def make_response(status_code=200, json_data=None):
    res = Response()
    res.status_code = status_code
    if json_data is not None:
        import json

        res._content = json.dumps(json_data).encode("utf-8")
    else:
        res._content = b""
    return res


def test_get_requests_401_raises_session_expired(monkeypatch):
    resp = make_response(status_code=401)

    def fake_get(*args, **kwargs):
        return resp

    # Patch the requests.get used inside the api_client module
    monkeypatch.setattr(api_client.requests, "get", fake_get)

    # Ensure session_state supports .clear()
    monkeypatch.setattr(api_client.st, "session_state", {})

    with pytest.raises(api_client.SessionExpired):
        api_client.get_requests()
